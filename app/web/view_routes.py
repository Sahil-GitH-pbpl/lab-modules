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


@bp.route("/mindraymainform8am", methods=["GET", "POST"])
@login_required
def mindraymainform8am():
    record_id = request.values.get("id", type=int)
    if not record_id:
        flash("Missing record id", "error")
        return redirect(url_for("main.mindrayverification"))

    if request.method == "POST":
        execute(
            "UPDATE mindraybc SET status='1', verifiedby=%s, variftime=%s WHERE timerec='eightam' AND id=%s",
            (session.get("empname", ""), now_str(), record_id),
        )
        flash("Record verified successfully.", "success")
        return redirect(url_for("main.mindrayverification"))

    row = fetch_one("SELECT * FROM mindraybc WHERE timerec='eightam' AND id=%s LIMIT 1", (record_id,))
    if not row:
        flash("Record not found", "error")
        return redirect(url_for("main.mindrayverification"))

    fields = detail_rows_from_config("mindray8am", row)
    return render_template(
        "detail_page.html",
        title="Mindray BC -780 - 8AM",
        time_label="8 AM",
        datetime_value=as_datetime_label(row.get("datetime")),
        fields=fields,
        can_verify=str(row.get("status", "0")) != "1",
        back_url=url_for("main.mindrayverification"),
    )


@bp.route("/mindraymainform4pm", methods=["GET", "POST"])
@login_required
def mindraymainform4pm():
    record_id = request.values.get("id", type=int)
    if not record_id:
        flash("Missing record id", "error")
        return redirect(url_for("main.mindrayverification"))

    if request.method == "POST":
        execute(
            "UPDATE mindraybc SET status='1', verifiedby=%s, variftime=%s WHERE timerec='fourpm' AND id=%s",
            (session.get("empname", ""), now_str(), record_id),
        )
        flash("Record verified successfully.", "success")
        return redirect(url_for("main.mindrayverification"))

    row = fetch_one("SELECT * FROM mindraybc WHERE timerec='fourpm' AND id=%s LIMIT 1", (record_id,))
    if not row:
        flash("Record not found", "error")
        return redirect(url_for("main.mindrayverification"))

    fields = detail_rows_from_config("mindray4pm", row)
    return render_template(
        "detail_page.html",
        title="Mindray BC -780 - 4PM",
        time_label="4 PM",
        datetime_value=as_datetime_label(row.get("datetime")),
        fields=fields,
        can_verify=str(row.get("status", "0")) != "1",
        back_url=url_for("main.mindrayverification"),
    )


@bp.route("/view/mindraybc7008am")
@login_required
def view_mindraybc7008am():
    return render_read_only_form("mindraybc7008am", "main.mindraybc700verification")


@bp.route("/mindraybc700mainform", methods=["GET", "POST"])
@login_required
def mindraybc700mainform():
    record_id = request.values.get("id", type=int)
    if not record_id:
        flash("Missing record id", "error")
        return redirect(url_for("main.mindraybc700verification"))

    if request.method == "POST":
        execute(
            "UPDATE mindraybc700 SET status='1', verifiedby=%s, variftime=%s WHERE id=%s",
            (session.get("empname", ""), now_str(), record_id),
        )
        flash("Record verified successfully.", "success")
        return redirect(url_for("main.mindraybc700verification"))

    row = fetch_one("SELECT * FROM mindraybc700 WHERE id=%s LIMIT 1", (record_id,))
    if not row:
        flash("Record not found", "error")
        return redirect(url_for("main.mindraybc700verification"))

    fields = detail_rows_from_config("mindraybc7008am", row)
    return render_template(
        "detail_page.html",
        title="Mindray BC 700 Detail",
        time_label="8 AM",
        datetime_value=as_datetime_label(row.get("datetime")),
        fields=fields,
        can_verify=str(row.get("status", "0")) != "1",
        back_url=url_for("main.mindraybc700verification"),
    )


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


@bp.route("/view/lifotronic-daily")
@login_required
def view_lifotronic_daily():
    return render_read_only_form("lifotronic_daily", "main.lifotronicverification")


@bp.route("/view/lifotronic-weekly")
@login_required
def view_lifotronic_weekly():
    return render_read_only_form("lifotronic_weekly", "main.lifotronicverification")


@bp.route("/view/laurav2-daily")
@login_required
def view_laurav2_daily():
    return render_read_only_form("laurav2_daily", "main.laurav2_verification")


@bp.route("/view/laurav2-weekly")
@login_required
def view_laurav2_weekly():
    return render_read_only_form("laurav2_weekly", "main.laurav2_verification")


@bp.route("/view/ecl760-daily")
@login_required
def view_ecl760_daily():
    return render_read_only_form("ecl760_daily", "main.ecl760_verification")


@bp.route("/view/maglumi800-daily")
@login_required
def view_maglumi800_daily():
    return render_read_only_form("maglumi800_daily", "main.maglumi800_verification")


def render_daily_equipment_detail(
    form_key: str,
    table: str,
    title: str,
    verification_endpoint: str,
):
    record_id = request.values.get("id", type=int)
    if not record_id:
        flash("Missing record id", "error")
        return redirect(url_for(verification_endpoint))

    if request.method == "POST":
        execute(
            f"UPDATE {table} "
            "SET status='1', verifiedby=%s, approvedby=%s, variftime=%s "
            "WHERE id=%s",
            (session.get("empname", ""), session.get("empname", ""), now_str(), record_id),
        )
        flash("Record verified successfully.", "success")
        return redirect(url_for(verification_endpoint))

    row = fetch_one(f"SELECT * FROM {table} WHERE id=%s", (record_id,))
    if not row:
        flash("Record not found", "error")
        return redirect(url_for(verification_endpoint))

    fields = detail_rows_from_config(form_key, row)
    return render_template(
        "detail_page.html",
        title=title,
        time_label="8 AM",
        datetime_value=as_datetime_label(row.get("datetime")),
        fields=fields,
        can_verify=str(row.get("status", "0")) != "1",
        back_url=url_for(verification_endpoint),
    )


@bp.route("/ecl760dailymainform", methods=["GET", "POST"])
@login_required
def ecl760dailymainform():
    return render_daily_equipment_detail(
        "ecl760_daily",
        "ecl760_daily",
        "ECL 760 Daily Detail",
        "main.ecl760_verification",
    )


@bp.route("/maglumi800dailymainform", methods=["GET", "POST"])
@login_required
def maglumi800dailymainform():
    return render_daily_equipment_detail(
        "maglumi800_daily",
        "maglumi800_daily",
        "Maglumi 800 Daily Detail",
        "main.maglumi800_verification",
    )


@bp.route("/lifotronicmainform", methods=["GET", "POST"])
@login_required
def lifotronicmainform():
    record_id = request.values.get("id", type=int)
    if not record_id:
        flash("Missing record id", "error")
        return redirect(url_for("main.lifotronicverification"))

    if request.method == "POST":
        execute(
            "UPDATE lifotronic_h100_daily "
            "SET status='1', verifiedby=%s, approvedby=%s, variftime=%s "
            "WHERE id=%s",
            (session.get("empname", ""), session.get("empname", ""), now_str(), record_id),
        )
        flash("Record verified successfully.", "success")
        return redirect(url_for("main.lifotronicverification"))

    row = fetch_one("SELECT * FROM lifotronic_h100_daily WHERE id=%s", (record_id,))
    if not row:
        flash("Record not found", "error")
        return redirect(url_for("main.lifotronicverification"))

    fields = detail_rows_from_config("lifotronic_daily", row)
    return render_template(
        "detail_page.html",
        title="LIFOTRONIC H100 Detail",
        time_label="Daily",
        datetime_value=as_datetime_label(row.get("created_at")),
        fields=fields,
        can_verify=str(row.get("status", "0")) != "1",
        back_url=url_for("main.lifotronicverification"),
    )


@bp.route("/laurav2dailymainform", methods=["GET", "POST"])
@login_required
def laurav2dailymainform():
    record_id = request.values.get("id", type=int)
    if not record_id:
        flash("Missing record id", "error")
        return redirect(url_for("main.laurav2_verification"))

    if request.method == "POST":
        execute(
            "UPDATE laurav2_daily "
            "SET status='1', verifiedby=%s, approvedby=%s, variftime=%s "
            "WHERE id=%s",
            (session.get("empname", ""), session.get("empname", ""), now_str(), record_id),
        )
        flash("Record verified successfully.", "success")
        return redirect(url_for("main.laurav2_verification"))

    row = fetch_one("SELECT * FROM laurav2_daily WHERE id=%s", (record_id,))
    if not row:
        flash("Record not found", "error")
        return redirect(url_for("main.laurav2_verification"))

    fields = detail_rows_from_config("laurav2_daily", row)
    return render_template(
        "detail_page.html",
        title="LAURA V2 Daily Detail",
        time_label="Daily",
        datetime_value=as_datetime_label(row.get("datetime")),
        fields=fields,
        can_verify=str(row.get("status", "0")) != "1",
        back_url=url_for("main.laurav2_verification"),
    )


@bp.route("/laurav2weeklymainform", methods=["GET", "POST"])
@login_required
def laurav2weeklymainform():
    record_id = request.values.get("id", type=int)
    if not record_id:
        flash("Missing record id", "error")
        return redirect(url_for("main.laurav2_verification"))

    if request.method == "POST":
        execute(
            "UPDATE laurav2_weekly "
            "SET status='1', verifiedby=%s, approvedby=%s, variftime=%s "
            "WHERE id=%s",
            (session.get("empname", ""), session.get("empname", ""), now_str(), record_id),
        )
        flash("Record verified successfully.", "success")
        return redirect(url_for("main.laurav2_verification"))

    row = fetch_one("SELECT * FROM laurav2_weekly WHERE id=%s", (record_id,))
    if not row:
        flash("Record not found", "error")
        return redirect(url_for("main.laurav2_verification"))

    fields = detail_rows_from_config("laurav2_weekly", row)
    return render_template(
        "detail_page.html",
        title="LAURA V2 Weekly Detail",
        time_label="Weekly",
        datetime_value=as_datetime_label(row.get("datetime")),
        fields=fields,
        can_verify=str(row.get("status", "0")) != "1",
        back_url=url_for("main.laurav2_verification"),
    )


@bp.route("/lifotronicweeklymainform", methods=["GET", "POST"])
@login_required
def lifotronicweeklymainform():
    record_id = request.values.get("id", type=int)
    if not record_id:
        flash("Missing record id", "error")
        return redirect(url_for("main.lifotronicverification"))

    if request.method == "POST":
        execute(
            "UPDATE lifotronic_h100_weekly "
            "SET status='1', verifiedby=%s, approvedby=%s, variftime=%s "
            "WHERE id=%s",
            (session.get("empname", ""), session.get("empname", ""), now_str(), record_id),
        )
        flash("Record verified successfully.", "success")
        return redirect(url_for("main.lifotronicverification"))

    row = fetch_one("SELECT * FROM lifotronic_h100_weekly WHERE id=%s", (record_id,))
    if not row:
        flash("Record not found", "error")
        return redirect(url_for("main.lifotronicverification"))

    fields = detail_rows_from_config("lifotronic_weekly", row)
    return render_template(
        "detail_page.html",
        title="LIFOTRONIC H100 Weekly Detail",
        time_label="Weekly",
        datetime_value=as_datetime_label(row.get("created_at")),
        fields=fields,
        can_verify=str(row.get("status", "0")) != "1",
        back_url=url_for("main.lifotronicverification"),
    )


@bp.route("/cobaspurelists", methods=["GET", "POST"])
@login_required
def cobaspurelists():
    return render_cobas_detail("cobaspure8am", "eightam", "Cobas Pure C-303/E402 Detail")


@bp.route("/cobaslistsevenpm", methods=["GET", "POST"])
@login_required
def cobaslistsevenpm():
    return render_cobas_detail("cobaspure7pm", "sevenpm", "Cobas Pure C-303/E402 Detail")


@bp.route("/cobaspureonethirtylist", methods=["GET", "POST"])
@login_required
def cobaspureonethirtylist():
    return render_cobas_detail("cobaspure130am", "onethirtyam", "Cobas Pure C-303/E402 Detail")


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
        back_url=url_for("main.aclelitemaint"),
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
