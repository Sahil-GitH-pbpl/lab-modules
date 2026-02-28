from datetime import datetime

from flask import render_template, url_for

from .blueprint import bp, login_required
from .helpers import pending_counts, today_slot_fill_state


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

    return render_template("dashboard.html", machine_summaries=summaries)


@bp.route("/temperature")
@login_required
def temperature():
    return render_template(
        "temperature_page.html",
        title="Temperature",
        target_url="http://192.168.0.110:3003",
    )
