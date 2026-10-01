from datetime import datetime
from zoneinfo import ZoneInfo

from flask import flash, redirect, render_template, request, session

from ..forms_config import FORM_CONFIGS
from .blueprint import bp, login_required
from .helpers import collect_request_values, group_fields, insert_form_record, slot_already_submitted_today


def render_form(form_key: str):
    config = FORM_CONFIGS[form_key]

    if request.method == "POST":
        if form_key == "lifotronic_weekly" and datetime.now(ZoneInfo("Asia/Kolkata")).weekday() != 0:
            flash("Weekly form can be submitted only on Monday.", "error")
            return redirect(request.path)
        if slot_already_submitted_today(form_key):
            flash("Today's form for this time slot is already submitted.", "error")
            return redirect(request.path)
        form_data = collect_request_values(config)
        insert_form_record(form_key, form_data)
        flash("Form submitted successfully.", "success")
        return redirect(request.path)

    record_meta = ""
    if config.get("username_column") == "documentedby":
        record_meta = f"Documented By: {session.get('empname', '')} | Approved By: Pending"

    return render_template(
        "form_page.html",
        title=config["title"],
        sections=group_fields(config["fields"]),
        read_only=False,
        field_values={},
        panel_subtitle=config.get("panel_subtitle", "Fill the checklist and submit."),
        record_meta=record_meta,
    )


@bp.route("/mindray8am", methods=["GET", "POST"])
@login_required
def mindray8am():
    return render_form("mindray8am")


@bp.route("/mindray4pm", methods=["GET", "POST"])
@login_required
def mindray4pm():
    return render_form("mindray4pm")


@bp.route("/mindraybc7008am", methods=["GET", "POST"])
@login_required
def mindraybc7008am():
    return render_form("mindraybc7008am")


@bp.route("/cobaspure8am", methods=["GET", "POST"])
@login_required
def cobaspure8am():
    return render_form("cobaspure8am")


@bp.route("/cobaspure7pm", methods=["GET", "POST"])
@login_required
def cobaspure7pm():
    return render_form("cobaspure7pm")


@bp.route("/cobaspure130am", methods=["GET", "POST"])
@login_required
def cobaspure130am():
    return render_form("cobaspure130am")


@bp.route("/attalica8am", methods=["GET", "POST"])
@login_required
def attalica8am():
    return render_form("attalica8am")


@bp.route("/attalica7pm", methods=["GET", "POST"])
@login_required
def attalica7pm():
    return render_form("attalica7pm")


@bp.route("/attalica12am", methods=["GET", "POST"])
@login_required
def attalica12am():
    return render_form("attalica12am")


@bp.route("/aclelite", methods=["GET", "POST"])
@login_required
def aclelite():
    return render_form("aclelite")


@bp.route("/lifotronic-daily-form", methods=["GET", "POST"])
@login_required
def lifotronic_daily_form():
    return render_form("lifotronic_daily")


@bp.route("/lifotronic-weekly-form", methods=["GET", "POST"])
@login_required
def lifotronic_weekly_form():
    return render_form("lifotronic_weekly")


@bp.route("/laurav2-daily-form", methods=["GET", "POST"])
@login_required
def laurav2_daily_form():
    return render_form("laurav2_daily")


# @bp.route("/laurav2-weekly-form", methods=["GET", "POST"])
# @login_required
# def laurav2_weekly_form():
#     return render_form("laurav2_weekly")
