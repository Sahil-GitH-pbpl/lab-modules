from flask import jsonify, flash, redirect, render_template, request, session, url_for

from ..db import execute, fetch_one
from .blueprint import bp, login_required
from .helpers import as_datetime_label, detail_rows_from_config, now_str, render_cobas_detail, render_read_only_form


@bp.route("/view/mindray8am")
@login_required
def view_mindray8am():
    return render_read_only_form("mindray8am", "main.mindrayverification")


@bp.route("/view/mindray4pm")
@login_required
def view_mindray4pm():
    return render_read_only_form("mindray4pm", "main.mindrayverification")


@bp.route("/view/cobaspure8am")
@login_required
def view_cobaspure8am():
    return render_read_only_form("cobaspure8am", "main.cobaspureall")


@bp.route("/view/cobaspure7pm")
@login_required
def view_cobaspure7pm():
    return render_read_only_form("cobaspure7pm", "main.cobaspureall")


@bp.route("/view/cobaspure130am")
@login_required
def view_cobaspure130am():
    return render_read_only_form("cobaspure130am", "main.cobaspureall")


@bp.route("/view/attalica8am")
@login_required
def view_attalica8am():
    return render_read_only_form("attalica8am", "main.attalicaverification")


@bp.route("/view/attalica7pm")
@login_required
def view_attalica7pm():
    return render_read_only_form("attalica7pm", "main.attalicaverification")


@bp.route("/view/attalica12am")
@login_required
def view_attalica12am():
    return render_read_only_form("attalica12am", "main.attalicaverification")


@bp.route("/view/aclelite")
@login_required
def view_aclelite():
    return render_read_only_form("aclelite", "main.aclelitemaint")


@bp.route("/cobaspurelists", methods=["GET", "POST"])
@login_required
def cobaspurelists():
    return render_cobas_detail("cobaspure8am", "eightam", "Cobas Pure Detail")


@bp.route("/cobaslistsevenpm", methods=["GET", "POST"])
@login_required
def cobaslistsevenpm():
    return render_cobas_detail("cobaspure7pm", "sevenpm", "Cobas Pure Detail")


@bp.route("/cobaspureonethirtylist", methods=["GET", "POST"])
@login_required
def cobaspureonethirtylist():
    return render_cobas_detail("cobaspure130am", "onethirtyam", "Cobas Pure Detail")


@bp.route("/aclelitemainform", methods=["GET", "POST"])
@login_required
def aclelitemainform():
    record_id = request.values.get("id", type=int)
    if not record_id:
        flash("Missing record id", "error")
        return redirect(url_for("main.aclelitemaint"))

    if request.method == "POST":
        execute(
            "UPDATE aclelite SET status='1', verifiedby=%s, variftime=%s WHERE id=%s",
            (session.get("empname", ""), now_str(), record_id),
        )
        flash("Record verified successfully.", "success")
        return redirect(request.path + f"?id={record_id}")

    row = fetch_one("SELECT * FROM aclelite WHERE id=%s", (record_id,))
    if not row:
        flash("Record not found", "error")
        return redirect(url_for("main.aclelitemaint"))

    fields = detail_rows_from_config("aclelite", row)
    return render_template(
        "detail_page.html",
        title="ACL Elite Detail",
        time_label="8 AM",
        datetime_value=as_datetime_label(row.get("datetimess")),
        fields=fields,
        can_verify=str(row.get("status", "0")) != "1",
    )


@bp.route("/attlicaver", methods=["POST"])
@login_required
def attlicaver():
    body = request.get_json(silent=True) or request.form
    row_id = body.get("nid") if hasattr(body, "get") else None
    try:
        row_id = int(row_id)
    except (TypeError, ValueError):
        row_id = None
    if not row_id:
        return jsonify({"ok": False, "error": "Missing id"}), 400

    execute(
        "UPDATE attalica SET status='1', verifiedby=%s, variftime=%s WHERE id=%s",
        (session.get("empname", ""), now_str(), row_id),
    )
    return jsonify({"ok": True})
