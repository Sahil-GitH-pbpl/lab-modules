from datetime import datetime

from flask import render_template, url_for

from .blueprint import bp, login_required
from .helpers import (
    pending_counts,
    pending_counts_simple,
    today_slot_fill_state,
    today_slot_fill_state_simple,
)


@bp.route("/dashboard")
@login_required
def dashboard():
    today_iso = datetime.now().strftime("%Y-%m-%d")
    machines = [
        {
            "title": "Mindray Machine",
            "table": "mindraybc",
            "datetime_col": "datetime",
            "verify_endpoint": "main.mindrayverification",
            "slots": [
                ("eightam", "8 AM", "main.mindray8am"),
                ("fourpm", "4 PM", "main.mindray4pm"),
            ],
        },
        {
            "title": "Cobas Pure Machine",
            "table": "cobaspure",
            "datetime_col": "datetime",
            "verify_endpoint": "main.cobaspureall",
            "slots": [
                ("onethirtyam", "1:30 AM", "main.cobaspure130am"),
                ("eightam", "8 AM", "main.cobaspure8am"),
                ("sevenpm", "7 PM", "main.cobaspure7pm"),
            ],
        },
        {
            "title": "Attalica Machine",
            "table": "attalica",
            "datetime_col": "datetime",
            "verify_endpoint": "main.attalicaverification",
            "slots": [
                ("twelvethirtyam", "12:30 AM", "main.attalica12am"),
                ("eightam", "8 AM", "main.attalica8am"),
                ("sevenpm", "7 PM", "main.attalica7pm"),
            ],
        },
        {
            "title": "ACL Elite Machine",
            "table": "aclelite",
            "datetime_col": "datetimess",
            "verify_endpoint": "main.aclelitemaint",
            "slots": [
                ("eightam", "8 AM", "main.aclelite"),
            ],
        },
    ]
    summaries = []
    for machine in machines:
        slot_items = []
        for timerec, label, fill_endpoint in machine["slots"]:
            state_text, state_class = today_slot_fill_state(
                machine["table"], machine["datetime_col"], timerec
            )
            slot_items.append(
                {
                    "label": label,
                    "state_text": state_text,
                    "state_class": state_class,
                    "fill_url": url_for(fill_endpoint),
                }
            )

        today_pending, total_pending = pending_counts(machine["table"], machine["datetime_col"])
        summaries.append(
            {
                "title": machine["title"],
                "slots": slot_items,
                "today_pending": today_pending,
                "total_pending": total_pending,
                "today_pending_url": url_for(
                    machine["verify_endpoint"], date1=today_iso, date2=today_iso
                ),
                "total_pending_url": url_for(machine["verify_endpoint"]),
            }
        )

    lifotronic_slots = [
        ("Daily", "main.lifotronic_daily_form", "lifotronic_h100_daily", "created_at"),
        ("Weekly", "main.lifotronic_weekly_form", "lifotronic_h100_weekly", "created_at"),
    ]
    lifotronic_slot_items = []
    for label, fill_endpoint, table, datetime_col in lifotronic_slots:
        state_text, state_class = today_slot_fill_state_simple(table, datetime_col)
        lifotronic_slot_items.append(
            {
                "label": label,
                "state_text": state_text,
                "state_class": state_class,
                "fill_url": url_for(fill_endpoint),
            }
        )
    l_today_1, l_total_1 = pending_counts_simple("lifotronic_h100_daily", "created_at")
    l_today_2, l_total_2 = pending_counts_simple("lifotronic_h100_weekly", "created_at")
    summaries.append(
        {
            "title": "LIFOTRONIC H100",
            "slots": lifotronic_slot_items,
            "today_pending": l_today_1 + l_today_2,
            "total_pending": l_total_1 + l_total_2,
            "today_pending_url": url_for("main.lifotronicverification", date1=today_iso, date2=today_iso),
            "total_pending_url": url_for("main.lifotronicverification"),
        }
    )

    laura_slots = [
        ("Daily", "main.laurav2_daily_form", "laurav2_daily", "created_at"),
        ("Weekly", "main.laurav2_weekly_form", "laurav2_weekly", "created_at"),
    ]
    laura_slot_items = []
    for label, fill_endpoint, table, datetime_col in laura_slots:
        state_text, state_class = today_slot_fill_state_simple(table, datetime_col)
        laura_slot_items.append(
            {
                "label": label,
                "state_text": state_text,
                "state_class": state_class,
                "fill_url": url_for(fill_endpoint),
            }
        )
    a_today_1, a_total_1 = pending_counts_simple("laurav2_daily", "created_at")
    a_today_2, a_total_2 = pending_counts_simple("laurav2_weekly", "created_at")
    summaries.append(
        {
            "title": "LAURA V2",
            "slots": laura_slot_items,
            "today_pending": a_today_1 + a_today_2,
            "total_pending": a_total_1 + a_total_2,
            "today_pending_url": url_for("main.laurav2_verification", date1=today_iso, date2=today_iso),
            "total_pending_url": url_for("main.laurav2_verification"),
        }
    )

    return render_template("dashboard.html", machine_summaries=summaries)


@bp.route("/temperature")
@login_required
def temperature():
    return render_template(
        "temperature_page.html",
        title="Temperature",
        target_url="http://192.168.0.110:3003",
    )
