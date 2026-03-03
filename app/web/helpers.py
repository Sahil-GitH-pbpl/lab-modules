from __future__ import annotations

from datetime import datetime
import re
from typing import Any

from flask import flash, redirect, render_template, request, session, url_for

from ..db import execute, fetch_all, fetch_one
from ..forms_config import FORM_CONFIGS, TIME_LABELS


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %I:%M %p")


def digits_only(value: str) -> str:
    return "".join(ch for ch in str(value) if ch.isdigit())


def as_date_label(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.strftime("%d-%m-%Y")

    raw = str(value).strip()
    for fmt in ("%Y-%m-%d %I:%M %p", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw, fmt).strftime("%d-%m-%Y")
        except ValueError:
            continue
    return raw


def as_datetime_label(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %I:%M %p")
    return str(value)


def status_meta(status_value: Any) -> tuple[str, str]:
    if str(status_value) == "1":
        return "Verified", "status-ok"
    return "Pending", "status-warn"


def today_slot_fill_state(table: str, datetime_col: str, timerec: str) -> tuple[str, str]:
    row = fetch_one(
        f"SELECT status, formfill FROM {table} "
        f"WHERE DATE({datetime_col})=CURDATE() AND timerec=%s "
        f"ORDER BY {datetime_col} DESC LIMIT 1",
        (timerec,),
    )
    if not row:
        return "Not Fill", "slot-notfill"
    if str(row.get("formfill", "0")) == "1":
        return "Not Fill", "slot-notfill"
    return "Filled", "slot-filled"


def pending_counts(table: str, datetime_col: str) -> tuple[int, int]:
    today_row = fetch_one(
        f"SELECT COUNT(*) AS cnt FROM {table} "
        f"WHERE DATE({datetime_col})=CURDATE() "
        "AND COALESCE(status, '0') <> '1' "
        "AND COALESCE(formfill, '0') <> '1'"
    ) or {}
    total_row = fetch_one(
        f"SELECT COUNT(*) AS cnt FROM {table} "
        "WHERE COALESCE(status, '0') <> '1' "
        "AND COALESCE(formfill, '0') <> '1'"
    ) or {}
    return int(today_row.get("cnt") or 0), int(total_row.get("cnt") or 0)


def today_slot_fill_state_simple(table: str, datetime_col: str) -> tuple[str, str]:
    try:
        row = fetch_one(
            f"SELECT 1 AS found FROM {table} "
            f"WHERE DATE({datetime_col})=CURDATE() "
            f"ORDER BY {datetime_col} DESC LIMIT 1"
        )
    except Exception:
        return "Not Fill", "slot-notfill"
    if not row:
        return "Not Fill", "slot-notfill"
    return "Filled", "slot-filled"


def pending_counts_simple(table: str, datetime_col: str) -> tuple[int, int]:
    try:
        today_row = fetch_one(
            f"SELECT COUNT(*) AS cnt FROM {table} "
            f"WHERE DATE({datetime_col})=CURDATE() "
            "AND COALESCE(status, '0') <> '1'"
        ) or {}
        total_row = fetch_one(
            f"SELECT COUNT(*) AS cnt FROM {table} "
            "WHERE COALESCE(status, '0') <> '1'"
        ) or {}
    except Exception:
        return 0, 0
    return int(today_row.get("cnt") or 0), int(total_row.get("cnt") or 0)


def group_fields(fields: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for field in fields:
        section = field.get("section", "Checklist")
        grouped.setdefault(section, []).append(field)
    return [{"title": k, "fields": v} for k, v in grouped.items()]


def strip_leading_index(label: str) -> str:
    # Convert labels like "1. Check ..." to "Check ..." for numbered-table views.
    return re.sub(r"^\s*\d+\.\s*", "", str(label or "")).strip()


def insert_form_record(form_key: str, form_data: dict[str, Any]) -> None:
    config = FORM_CONFIGS[form_key]

    columns: list[str] = []
    params: list[Any] = []

    for input_name, col_name in config["column_map"].items():
        columns.append(col_name)
        params.append(form_data.get(input_name, ""))

    dt_col = config.get("datetime_column")
    if dt_col:
        columns.append(dt_col)
        params.append(now_str())

    user_col = config.get("username_column")
    if user_col:
        columns.append(user_col)
        params.append(session.get("empname", ""))

    for col_name, col_value in config.get("fixed_columns", {}).items():
        columns.append(col_name)
        params.append(col_value)

    if config.get("timerec"):
        columns.append("timerec")
        params.append(config["timerec"])

    if config.get("submitform") is not None:
        columns.append("submitform")
        params.append(str(config["submitform"]))

    col_sql = ", ".join(f"`{c}`" for c in columns)
    placeholders = ", ".join(["%s"] * len(columns))
    sql = f"INSERT INTO {config['table']} ({col_sql}) VALUES ({placeholders})"
    execute(sql, tuple(params))


def collect_request_values(config: dict[str, Any]) -> dict[str, str]:
    data: dict[str, str] = {}
    for field in config["fields"]:
        key = field["name"]
        if field["type"] == "checkbox":
            data[key] = "yes" if request.form.get(key) else ""
        elif field["type"] == "number":
            data[key] = digits_only(request.form.get(key, "").strip())
        else:
            data[key] = request.form.get(key, "").strip()
    return data


def field_values_from_row(form_key: str, row: dict[str, Any]) -> dict[str, str]:
    config = FORM_CONFIGS[form_key]
    values: dict[str, str] = {}
    for input_name, col_name in config["column_map"].items():
        value = row.get(col_name, "")
        values[input_name] = "" if value is None else str(value)
    return values


def render_read_only_form(form_key: str, fallback_endpoint: str):
    config = FORM_CONFIGS[form_key]
    record_id = request.values.get("id", type=int)
    if not record_id:
        flash("Missing record id", "error")
        return redirect(url_for(fallback_endpoint))

    where = ["id=%s"]
    params: list[Any] = [record_id]
    if config.get("timerec"):
        where.append("timerec=%s")
        params.append(config["timerec"])

    sql = f"SELECT * FROM {config['table']} WHERE {' AND '.join(where)} LIMIT 1"
    row = fetch_one(sql, tuple(params))
    if not row:
        flash("Record not found", "error")
        return redirect(url_for(fallback_endpoint))

    filled_by_col = config.get("username_column") or "username"
    filled_by = str(row.get(filled_by_col) or row.get("username") or "").strip() or "Unknown"
    verified_by = str(row.get("verifiedby") or "").strip() or "Pending"
    datetime_col = config.get("datetime_column", "")
    filled_at = as_datetime_label(row.get(datetime_col, "")) if datetime_col else ""
    time_label = TIME_LABELS.get(config["timerec"], config["timerec"]) if config.get("timerec") else ""

    sections = group_fields(config["fields"])
    for section in sections:
        for field in section["fields"]:
            field["display_label"] = strip_leading_index(field.get("label", ""))

    return render_template(
        "form_view_pdf.html",
        title=config["title"],
        sections=sections,
        field_values=field_values_from_row(form_key, row),
        filled_by=filled_by,
        verified_by=verified_by,
        filled_at=filled_at,
        time_label=time_label,
        back_url=url_for(fallback_endpoint),
    )


def filtered_rows(table: str, datetime_col: str, allow_time: bool = True):
    date1 = (request.values.get("date1") or "").strip()
    date2 = (request.values.get("date2") or "").strip()
    timerec = (request.values.get("timerec") or "").strip()
    page_raw = (request.values.get("page") or "").strip().lower()
    is_all = page_raw == "all"
    page = 1
    if not is_all:
        try:
            page = int(page_raw) if page_raw else 1
        except ValueError:
            page = 1
        if page < 1:
            page = 1
    per_page = 20

    where = []
    params: list[Any] = []

    if date1 and date2:
        where.append(f"DATE({datetime_col}) BETWEEN %s AND %s")
        params.extend([date1, date2])

    if allow_time and timerec:
        where.append("timerec=%s")
        params.append(timerec)

    where_sql = ""
    if where:
        where_sql = " WHERE " + " AND ".join(where)

    count_sql = f"SELECT COUNT(*) AS total FROM {table}{where_sql}"
    total_row = fetch_one(count_sql, tuple(params)) or {}
    total_records = int(total_row.get("total") or 0)

    if is_all:
        per_page = total_records if total_records > 0 else 1
        total_pages = 1
        page = 1
    else:
        total_pages = max((total_records + per_page - 1) // per_page, 1)
        if page > total_pages:
            page = total_pages

    order_sql = f" ORDER BY {datetime_col} ASC" if where else f" ORDER BY {datetime_col} DESC"
    offset = (page - 1) * per_page
    data_sql = f"SELECT * FROM {table}{where_sql}{order_sql} LIMIT %s OFFSET %s"
    rows = fetch_all(data_sql, tuple(params + [per_page, offset]))

    if total_records:
        start_index = offset + 1
        end_index = min(offset + len(rows), total_records)
    else:
        start_index = 0
        end_index = 0

    page_window_start = max(1, page - 2)
    page_window_end = min(total_pages, page + 2)
    pagination = {
        "page": page,
        "per_page": per_page,
        "total_records": total_records,
        "total_pages": total_pages,
        "has_prev": page > 1,
        "has_next": (page < total_pages) and (not is_all),
        "prev_page": page - 1,
        "next_page": page + 1,
        "pages": list(range(page_window_start, page_window_end + 1)) if not is_all else [1],
        "start_index": start_index,
        "end_index": end_index,
        "is_all": is_all,
    }

    return rows, date1, date2, timerec, pagination


def detail_rows_from_config(form_key: str, row: dict[str, Any]):
    config = FORM_CONFIGS[form_key]
    fields = []
    for field in config["fields"]:
        col = config["column_map"][field["name"]]
        value = row.get(col, "")
        fields.append(
            {
                "section": field.get("section", "Checklist"),
                "label": field["label"],
                "type": field["type"],
                "value": value,
                "checked": str(value).lower() == "yes",
            }
        )
    return fields


def render_cobas_detail(form_key: str, timerec: str, title: str):
    record_id = request.values.get("id", type=int)
    if not record_id:
        flash("Missing record id", "error")
        return redirect(url_for("main.cobaspureall"))

    if request.method == "POST":
        execute(
            "UPDATE cobaspure SET status='1', verifiedby=%s, variftime=%s WHERE timerec=%s AND id=%s",
            (session.get("empname", ""), now_str(), timerec, record_id),
        )
        flash("Record verified successfully.", "success")
        return redirect(request.path + f"?id={record_id}")

    row = fetch_one("SELECT * FROM cobaspure WHERE timerec=%s AND id=%s", (timerec, record_id))
    if not row:
        flash("Record not found", "error")
        return redirect(url_for("main.cobaspureall"))

    fields = detail_rows_from_config(form_key, row)
    return render_template(
        "detail_page.html",
        title=title,
        time_label=TIME_LABELS.get(timerec, timerec),
        datetime_value=as_datetime_label(row.get("datetime")),
        fields=fields,
        can_verify=str(row.get("status", "0")) != "1",
        back_url=url_for("main.cobaspureall"),
    )
