#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, date, time, timedelta
from typing import Any
from zoneinfo import ZoneInfo
from urllib import request, error

import pymysql

IST = ZoneInfo("Asia/Kolkata")

API_URL = os.getenv("INTIMATION_API_URL", "http://10.1.1.181:3004/api/messages/send")
GROUP_ID = os.getenv("INTIMATION_GROUP_ID", "120363419496643413@g.us")
ACCOUNT_ID = os.getenv("INTIMATION_ACCOUNT_ID", "1")
GRACE_HOURS = int(os.getenv("INTIMATION_GRACE_HOURS", "2"))
API_TIMEOUT_SECONDS = int(os.getenv("INTIMATION_API_TIMEOUT", "10"))

DB_HOST = os.getenv("LABMOD_DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("LABMOD_DB_PORT", "3310"))
DB_USER = os.getenv("LABMOD_DB_USER", "labmod")
DB_PASSWORD = os.getenv("LABMOD_DB_PASSWORD", "labmod_pass_123")
DB_NAME = os.getenv("LABMOD_DB_NAME", "laboratry_module_db")


@dataclass(frozen=True)
class SlotConfig:
    machine_key: str
    machine_label: str
    table: str
    date_col: str
    slot_code: str
    slot_label: str
    slot_time: str  # HH:MM 24h
    timerec: str | None = None
    check_formfill: bool = False
    grace_hours: int | None = None


# Weekly forms intentionally excluded.
SLOTS: list[SlotConfig] = [
    SlotConfig("mindray", "Mindray BC -780", "mindraybc", "datetime", "eightam", "8 AM", "08:00", "eightam", True),
    SlotConfig("mindray", "Mindray BC -780", "mindraybc", "datetime", "fourpm", "4 PM", "16:00", "fourpm", True),
    SlotConfig("mindraybc700", "Mindray BC700", "mindraybc700", "datetime", "eightam", "8 AM", "08:00", "eightam", True),
    SlotConfig("cobaspure", "Cobas Pure C-303/E402", "cobaspure", "datetime", "onethirtyam", "1:30 AM", "01:30", "onethirtyam", True),
    SlotConfig("cobaspure", "Cobas Pure C-303/E402", "cobaspure", "datetime", "eightam", "8 AM", "08:00", "eightam", True),
    SlotConfig("cobaspure", "Cobas Pure C-303/E402", "cobaspure", "datetime", "sevenpm", "7 PM", "19:00", "sevenpm", True),
    SlotConfig("attalica", "Siemens Attelica CI 1900", "attalica", "datetime", "twelvethirtyam", "12:30 AM", "00:30", "twelvethirtyam", True),
    SlotConfig("attalica", "Siemens Attelica CI 1900", "attalica", "datetime", "eightam", "8 AM", "08:00", "eightam", True),
    SlotConfig("attalica", "Siemens Attelica CI 1900", "attalica", "datetime", "sevenpm", "7 PM", "19:00", "sevenpm", True),
    SlotConfig("aclelite", "ACL Elite", "aclelite", "datetimess", "eightam", "8 AM", "08:00", "eightam", True),
    SlotConfig("lifotronic", "LIFOTRONIC H100", "lifotronic_h100_daily", "created_at", "nineam", "9 AM", "09:00", None, False),
    SlotConfig("laurav2", "LAURA V2", "laurav2_daily", "created_at", "nineam", "9 AM", "09:00", None, False),
    SlotConfig("sample_discard", "Sample Discard", "sample_discard", "discarded_at", "daily", "Daily", "14:00", None, False, 0),
]


def db_conn() -> pymysql.connections.Connection:
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


def ensure_log_table(conn: pymysql.connections.Connection) -> None:
    sql = """
    CREATE TABLE IF NOT EXISTS form_intimation_log (
      id BIGINT NOT NULL AUTO_INCREMENT,
      slot_date DATE NOT NULL,
      machine_key VARCHAR(64) NOT NULL,
      slot_code VARCHAR(64) NOT NULL,
      deadline_at DATETIME NOT NULL,
      sent_success TINYINT(1) NOT NULL DEFAULT 0,
      message_text TEXT NULL,
      api_response TEXT NULL,
      error_text TEXT NULL,
      sent_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
      PRIMARY KEY (id),
      UNIQUE KEY uq_slot_date_machine_slot (slot_date, machine_key, slot_code)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()


def today_deadline(today: date, slot_hhmm: str, grace_hours: int | None = None) -> datetime:
    hh, mm = [int(x) for x in slot_hhmm.split(":")]
    slot_dt = datetime.combine(today, time(hh, mm), tzinfo=IST)
    effective_grace_hours = GRACE_HOURS if grace_hours is None else grace_hours
    return slot_dt + timedelta(hours=effective_grace_hours)


def is_slot_filled(conn: pymysql.connections.Connection, slot: SlotConfig, slot_date: date) -> bool:
    date_str = slot_date.strftime("%Y-%m-%d")

    where_parts: list[str] = []
    params: list[Any] = []

    if slot.date_col == "datetime":
        where_parts.append("LEFT(datetime, 10)=%s")
    else:
        where_parts.append(f"DATE({slot.date_col})=%s")
    params.append(date_str)

    if slot.timerec:
        where_parts.append("timerec=%s")
        params.append(slot.timerec)

    if slot.check_formfill:
        where_parts.append("COALESCE(formfill, '0') <> '1'")

    sql = f"SELECT 1 AS found FROM {slot.table} WHERE {' AND '.join(where_parts)} ORDER BY id DESC LIMIT 1"

    with conn.cursor() as cur:
        cur.execute(sql, tuple(params))
        row = cur.fetchone()
    return bool(row)


def already_sent_success(conn: pymysql.connections.Connection, slot: SlotConfig, slot_date: date) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT 1 AS found
            FROM form_intimation_log
            WHERE slot_date=%s AND machine_key=%s AND slot_code=%s AND sent_success=1
            LIMIT 1
            """,
            (slot_date.strftime("%Y-%m-%d"), slot.machine_key, slot.slot_code),
        )
        return bool(cur.fetchone())


def upsert_log(
    conn: pymysql.connections.Connection,
    slot: SlotConfig,
    slot_date: date,
    deadline: datetime,
    sent_success: bool,
    message_text: str,
    api_response: str | None,
    error_text: str | None,
) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO form_intimation_log
              (slot_date, machine_key, slot_code, deadline_at, sent_success, message_text, api_response, error_text)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE
              deadline_at=VALUES(deadline_at),
              sent_success=VALUES(sent_success),
              message_text=VALUES(message_text),
              api_response=VALUES(api_response),
              error_text=VALUES(error_text),
              sent_at=CURRENT_TIMESTAMP
            """,
            (
                slot_date.strftime("%Y-%m-%d"),
                slot.machine_key,
                slot.slot_code,
                deadline.strftime("%Y-%m-%d %H:%M:%S"),
                1 if sent_success else 0,
                message_text,
                api_response,
                error_text,
            ),
        )
    conn.commit()


def send_group_message(message_text: str) -> tuple[bool, str | None, str | None]:
    payload = {
        "accountId": ACCOUNT_ID,
        "target": GROUP_ID,
        "message": message_text,
    }
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        API_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=API_TIMEOUT_SECONDS) as resp:
            text = resp.read().decode("utf-8", errors="replace")
            ok = 200 <= resp.status < 300
            return ok, text, None
    except error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else str(e)
        return False, detail, f"HTTPError: {e.code}"
    except Exception as e:  # noqa: BLE001
        return False, None, str(e)


def build_message(slot: SlotConfig, slot_date: date, deadline: datetime) -> str:
    return (
        f"Reminder: The {slot.machine_label} {slot.slot_label} form for "
        f"{slot_date.strftime('%d-%m-%Y')} is still not filled as of {deadline.strftime('%I:%M %p')}. "
        "Please fill it as soon as possible."
    )


def main() -> int:
    now = datetime.now(IST)
    today = now.date()

    print(f"[INTIMATION] now_ist={now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[INTIMATION] db={DB_HOST}:{DB_PORT}/{DB_NAME}")

    conn = db_conn()
    try:
        ensure_log_table(conn)

        checked = 0
        due = 0
        sent = 0
        already = 0
        filled = 0

        for slot in SLOTS:
            checked += 1
            deadline = today_deadline(today, slot.slot_time, slot.grace_hours)
            if now < deadline:
                continue
            due += 1

            if is_slot_filled(conn, slot, today):
                filled += 1
                continue

            if already_sent_success(conn, slot, today):
                already += 1
                continue

            message_text = build_message(slot, today, deadline)
            ok, api_resp, err_text = send_group_message(message_text)
            upsert_log(conn, slot, today, deadline, ok, message_text, api_resp, err_text)

            if ok:
                sent += 1
                print(f"[SENT] {slot.machine_label} {slot.slot_label}")
            else:
                print(f"[FAILED] {slot.machine_label} {slot.slot_label} err={err_text}")

        print(
            "[SUMMARY] "
            f"checked={checked} due={due} filled={filled} already_sent={already} sent_now={sent}"
        )
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
