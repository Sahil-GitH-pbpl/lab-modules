from __future__ import annotations

import os
import random
from datetime import date, datetime, time, timedelta

import pymysql


START_DATE = date(2025, 1, 1)
END_DATE = date(2026, 3, 1)
NAMES = [
    "GIRDHAR SINGH BORA",
    "Md Shaquib Alam",
    "Mansi Shukla",
    "Kanak lata Pallai",
    "Ravi Kumar Pandey",
    "Shreya",
    "Jyoti Marwah",
    "Manwar Singh negi",
    "VIMAL RANJAN PANDEY",
]


def connect():
    return pymysql.connect(
        host=os.getenv("LABMOD_DB_HOST", "host.docker.internal"),
        port=int(os.getenv("LABMOD_DB_PORT", "3310")),
        user=os.getenv("LABMOD_DB_USER", "labmod"),
        password=os.getenv("LABMOD_DB_PASSWORD", "labmod_pass_123"),
        database=os.getenv("LABMOD_DB_NAME", "laboratry_module_db"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


def daterange(start: date, end: date):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def monday_dates(start: date, end: date):
    for current in daterange(start, end):
        if current.weekday() == 0:
            yield current


def format_dt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %I:%M %p")


def next_counter_value(state: dict[str, int]) -> int:
    next_value = state["value"] - random.randint(45, 210)
    if next_value <= 120:
        next_value = random.randint(4625, 4945)
    state["value"] = next_value
    return next_value


def random_created_at(day: date, start_hour: int, end_hour: int) -> datetime:
    hour = random.randint(start_hour, end_hour)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return datetime.combine(day, time(hour=hour, minute=minute, second=second))


def seed_daily(cur):
    cur.execute(
        """
        SELECT DATE(created_at) AS day
        FROM lifotronic_h100_daily
        WHERE DATE(created_at) BETWEEN %s AND %s
        """,
        (START_DATE, END_DATE),
    )
    existing = {row["day"] for row in cur.fetchall()}
    counter_state = {"value": random.randint(4625, 4945)}
    inserted = 0

    for day in daterange(START_DATE, END_DATE):
        if day in existing:
            continue

        created_at = random_created_at(day, 7, 9)
        verified_at = created_at + timedelta(hours=random.randint(1, 10), minutes=random.randint(0, 59))
        documentedby = random.choice(NAMES)
        approvedby = random.choice(NAMES)
        column_count = next_counter_value(counter_state)
        filter_count = max(20, min(1200, int(column_count * random.uniform(0.08, 0.34))))

        cur.execute(
            """
            INSERT INTO lifotronic_h100_daily (
                reagent_volume_check,
                check_rt,
                column_count,
                filter_count,
                adc_check,
                pressure_check,
                documentedby,
                approvedby,
                datetime,
                created_at,
                status,
                verifiedby,
                variftime
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                "yes",
                "yes",
                column_count,
                filter_count,
                "yes",
                "yes",
                documentedby,
                approvedby,
                format_dt(created_at),
                created_at,
                "1",
                approvedby,
                format_dt(verified_at),
            ),
        )
        inserted += 1

    return inserted


def seed_weekly(cur):
    cur.execute(
        """
        SELECT DATE(created_at) AS day
        FROM lifotronic_h100_weekly
        WHERE DATE(created_at) BETWEEN %s AND %s
        """,
        (START_DATE, END_DATE),
    )
    existing = {row["day"] for row in cur.fetchall()}
    inserted = 0

    for day in monday_dates(START_DATE, END_DATE):
        if day in existing:
            continue

        created_at = random_created_at(day, 8, 18)
        verified_at = created_at + timedelta(minutes=random.randint(15, 240))
        documentedby = random.choice(NAMES)
        approvedby = random.choice(NAMES)

        cur.execute(
            """
            INSERT INTO lifotronic_h100_weekly (
                hp_pump_cleaning,
                diluting_tank_cleaning,
                probe_inner_well,
                probe_outer_well,
                clean_system,
                clean_sample_rack,
                clean_sample_holder,
                documentedby,
                approvedby,
                datetime,
                created_at,
                status,
                verifiedby,
                variftime
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                "yes",
                "yes",
                "yes",
                "yes",
                "yes",
                "yes",
                "yes",
                documentedby,
                approvedby,
                format_dt(created_at),
                created_at,
                "1",
                approvedby,
                format_dt(verified_at),
            ),
        )
        inserted += 1

    return inserted


def main():
    random.seed(20250406)
    conn = connect()
    try:
        with conn.cursor() as cur:
            daily_inserted = seed_daily(cur)
            weekly_inserted = seed_weekly(cur)
        conn.commit()
        print(
            f"Inserted daily={daily_inserted} weekly={weekly_inserted} "
            f"for range {START_DATE} to {END_DATE}"
        )
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
