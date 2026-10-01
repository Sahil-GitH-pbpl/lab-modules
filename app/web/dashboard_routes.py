from datetime import datetime
from zoneinfo import ZoneInfo

from flask import flash, redirect, render_template, request, url_for

from ..db import execute, fetch_all, fetch_one
from .blueprint import bp, login_required
from .helpers import (
    pending_counts,
    pending_counts_simple,
    today_slot_fill_state,
    today_slot_fill_state_simple,
    week_slot_fill_state_simple,
)

INCIDENT_NATURE_OPTIONS = (
    "Needle Stick Injury",
    "Sample Spill",
    "Reagent Spill",
    "Fall",
    "Electric Shock",
    "Burns",
    "Physical injury from non infectious material",
    "Fire",
    "Short Circuits",
    "Others",
    "Glass break",
)

REPORTED_TO_OPTIONS = (
    "Dr.Vishu Bhasin",
    "Salim Javed",
    "Dr Vipul Bhasin",
    "Rupa",
    "Vimal Ranjan pandey",
    "Dr Nitika Aggarwal",
)


def format_adverse_datetime(value):
    if not value:
        return "-"
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %I:%M %p")
    return str(value)


@bp.route("/dashboard")
@login_required
def dashboard():
    today_iso = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d")
    machines = [
        {
            "title": "Mindray BC -780",
            "table": "mindraybc",
            "datetime_col": "datetime",
            "verify_endpoint": "main.mindrayverification",
            "slots": [
                ("eightam", "8 AM", "main.mindray8am"),
                ("fourpm", "4 PM", "main.mindray4pm"),
            ],
        },
        {
            "title": "Mindray BC 700",
            "table": "mindraybc700",
            "datetime_col": "datetime",
            "verify_endpoint": "main.mindraybc700verification",
            "slots": [
                ("eightam", "8 AM", "main.mindraybc7008am"),
            ],
        },
        {
            "title": "Cobas Pure C-303/E402",
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
            "title": "Siemens Attelica CI 1900",
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
            "title": "ACL Elite",
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
        ("9 AM", "main.lifotronic_daily_form", "lifotronic_h100_daily", "created_at"),
        ("Monday", "main.lifotronic_weekly_form", "lifotronic_h100_weekly", "created_at"),
    ]
    lifotronic_slot_items = []
    for label, fill_endpoint, table, datetime_col in lifotronic_slots:
        if label == "Monday":
            state_text, state_class = week_slot_fill_state_simple(table, datetime_col)
        else:
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
        ("9 AM", "main.laurav2_daily_form", "laurav2_daily", "datetime"),
        # ("Weekly", "main.laurav2_weekly_form", "laurav2_weekly", "datetime"),  # disabled for now
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
    a_today_1, a_total_1 = pending_counts_simple("laurav2_daily", "datetime")
    # a_today_2, a_total_2 = pending_counts_simple("laurav2_weekly", "datetime")  # disabled for now
    summaries.append(
        {
            "title": "LAURA V2",
            "slots": laura_slot_items,
            "today_pending": a_today_1,
            "total_pending": a_total_1,
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
        target_url="http://10.1.1.150:3003",
    )


@bp.route("/adverse-instance-reporting", methods=["GET", "POST"])
@login_required
def adverse_instance_reporting():
    if request.method == "POST":
        incident_date = (request.form.get("incident_date") or "").strip()
        reporting_date = (request.form.get("reporting_date") or "").strip() or None
        incident_nature = (request.form.get("incident_nature") or "").strip() or None
        staff_involved = (request.form.get("staff_involved") or "").strip()
        incident_details = (request.form.get("incident_details") or "").strip() or None
        injury_hazard = (request.form.get("injury_hazard") or "").strip() or None
        corrective_action = (request.form.get("corrective_action") or "").strip() or None
        preventive_action = (request.form.get("preventive_action") or "").strip() or None
        matter_resolved = (request.form.get("matter_resolved") or "").strip() or None
        reported_to = (request.form.get("reported_to") or "").strip()

        if not incident_date:
            flash("Please select date of incident.", "error")
            return redirect(request.path)
        if not staff_involved:
            flash("Please enter staff involved.", "error")
            return redirect(request.path)
        if incident_nature and incident_nature not in INCIDENT_NATURE_OPTIONS:
            flash("Please select a valid nature of incident.", "error")
            return redirect(request.path)
        if injury_hazard and injury_hazard not in ("Yes", "No"):
            flash("Please select a valid injury/hazard option.", "error")
            return redirect(request.path)
        if matter_resolved and matter_resolved not in ("Yes", "No"):
            flash("Please select a valid matter resolved option.", "error")
            return redirect(request.path)
        if reported_to not in REPORTED_TO_OPTIONS:
            flash("Please select reported to.", "error")
            return redirect(request.path)

        execute(
            """
            INSERT INTO adverse_instance_reporting (
                incident_date,
                reporting_date,
                incident_nature,
                staff_involved,
                incident_details,
                injury_hazard,
                corrective_action,
                preventive_action,
                matter_resolved,
                reported_to
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                incident_date,
                reporting_date,
                incident_nature,
                staff_involved,
                incident_details,
                injury_hazard,
                corrective_action,
                preventive_action,
                matter_resolved,
                reported_to,
            ),
        )
        flash("Adverse incident report saved successfully.", "success")
        return redirect(request.path)

    return render_template(
        "adverse_instance_reporting.html",
        title="Adverse Instance Reporting",
        incident_nature_options=INCIDENT_NATURE_OPTIONS,
        reported_to_options=REPORTED_TO_OPTIONS,
    )


@bp.route("/adverse-instance-reports", methods=["GET"])
@login_required
def adverse_instance_reports():
    rows = fetch_all(
        """
        SELECT
            id,
            incident_date,
            reporting_date,
            incident_nature,
            staff_involved,
            incident_details,
            injury_hazard,
            corrective_action,
            preventive_action,
            matter_resolved,
            reported_to,
            created_at
        FROM adverse_instance_reporting
        ORDER BY created_at DESC, id DESC
        """
    )

    items = []
    for idx, row in enumerate(rows, start=1):
        items.append(
            {
                "sr": idx,
                "id": row.get("id"),
                "incident_date": row.get("incident_date"),
                "reporting_date": row.get("reporting_date"),
                "incident_nature": row.get("incident_nature") or "-",
                "staff_involved": row.get("staff_involved") or "-",
                "incident_details": row.get("incident_details") or "-",
                "injury_hazard": row.get("injury_hazard") or "-",
                "corrective_action": row.get("corrective_action") or "-",
                "preventive_action": row.get("preventive_action") or "-",
                "matter_resolved": row.get("matter_resolved") or "-",
                "reported_to": row.get("reported_to") or "-",
                "created_at": format_adverse_datetime(row.get("created_at")),
            }
        )

    return render_template(
        "adverse_instance_reports.html",
        title="Adverse Instance Reports",
        items=items,
    )


@bp.route("/adverse-instance-reports/<int:report_id>", methods=["GET"])
@login_required
def adverse_instance_report_detail(report_id: int):
    report = fetch_one(
        """
        SELECT
            id,
            incident_date,
            reporting_date,
            incident_nature,
            staff_involved,
            incident_details,
            injury_hazard,
            corrective_action,
            preventive_action,
            matter_resolved,
            reported_to,
            created_at
        FROM adverse_instance_reporting
        WHERE id = %s
        """,
        (report_id,),
    )
    if not report:
        flash("Adverse incident report not found.", "error")
        return redirect(url_for("main.adverse_instance_reports"))

    return render_template(
        "adverse_instance_report_detail.html",
        title="Adverse Incident Report Detail",
        report=report,
    )
