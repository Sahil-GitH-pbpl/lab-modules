from flask import flash, redirect, render_template, request

from ..forms_config import FORM_CONFIGS
from .blueprint import bp, login_required
from .helpers import collect_request_values, group_fields, insert_form_record


def render_form(form_key: str):
    config = FORM_CONFIGS[form_key]

    if request.method == "POST":
        form_data = collect_request_values(config)
        insert_form_record(form_key, form_data)
        flash("Form submitted successfully.", "success")
        return redirect(request.path)

    return render_template(
        "form_page.html",
        title=config["title"],
        sections=group_fields(config["fields"]),
        read_only=False,
        field_values={},
        panel_subtitle="Fill the checklist and submit.",
        record_meta="",
    )


@bp.route("/mindray8am", methods=["GET", "POST"])
@login_required
def mindray8am():
    return render_form("mindray8am")


@bp.route("/mindray4pm", methods=["GET", "POST"])
@login_required
def mindray4pm():
    return render_form("mindray4pm")


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
