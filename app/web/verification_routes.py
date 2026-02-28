from flask import render_template, url_for

from ..forms_config import TIME_LABELS
from .blueprint import bp, login_required
from .helpers import as_date_label, as_datetime_label, filtered_rows, status_meta


@bp.route("/mindrayverification", methods=["GET", "POST"])
@login_required
def mindrayverification():
    rows, date1, date2, timerec, pagination = filtered_rows("mindraybc", "datetime", allow_time=True)
    view_endpoint_by_time = {
        "eightam": "main.view_mindray8am",
        "fourpm": "main.view_mindray4pm",
    }

    items = []
    row_start = pagination["start_index"] if pagination["start_index"] else 1
    for idx, row in enumerate(rows, start=row_start):
        status_text, status_class = status_meta(row.get("status", "0"))
        record_time = str(row.get("timerec", ""))
        view_endpoint = view_endpoint_by_time.get(record_time)
        view_url = url_for(view_endpoint, id=row["id"]) if view_endpoint else ""
        status_url = view_url

        if str(row.get("formfill", "0")) == "1":
            status_text = "Not Fill"
            status_class = "status-muted"
            status_url = ""
            view_url = ""

        items.append(
            {
                "id": row["id"],
                "sr": idx,
                "date": as_date_label(row.get("datetime")),
                "datetime": as_datetime_label(row.get("datetime")),
                "time": TIME_LABELS.get(record_time, record_time),
                "status_text": status_text,
                "status_class": status_class,
                "status_url": status_url,
                "view_url": view_url,
            }
        )

    return render_template(
        "list_page.html",
        title="Mindray Verification",
        items=items,
        date1=date1,
        date2=date2,
        timerec=timerec,
        show_time_filter=True,
        time_options=[
            ("eightam", "8 AM"),
            ("fourpm", "4 PM"),
        ],
        pagination=pagination,
    )


@bp.route("/cobaspureall", methods=["GET", "POST"])
@login_required
def cobaspureall():
    rows, date1, date2, timerec, pagination = filtered_rows("cobaspure", "datetime", allow_time=True)

    detail_endpoint_by_time = {
        "eightam": "main.cobaspurelists",
        "sevenpm": "main.cobaslistsevenpm",
        "onethirtyam": "main.cobaspureonethirtylist",
    }
    view_endpoint_by_time = {
        "eightam": "main.view_cobaspure8am",
        "sevenpm": "main.view_cobaspure7pm",
        "onethirtyam": "main.view_cobaspure130am",
    }

    items = []
    row_start = pagination["start_index"] if pagination["start_index"] else 1
    for idx, row in enumerate(rows, start=row_start):
        status_text, status_class = status_meta(row.get("status", "0"))
        record_time = str(row.get("timerec", ""))
        endpoint = detail_endpoint_by_time.get(record_time)
        status_url = url_for(endpoint, id=row["id"]) if endpoint else ""
        view_endpoint = view_endpoint_by_time.get(record_time)
        view_url = url_for(view_endpoint, id=row["id"]) if view_endpoint else ""

        if str(row.get("formfill", "0")) == "1":
            status_text = "Not Fill"
            status_class = "status-muted"
            status_url = ""
            view_url = ""

        items.append(
            {
                "id": row["id"],
                "sr": idx,
                "date": as_date_label(row.get("datetime")),
                "datetime": as_datetime_label(row.get("datetime")),
                "time": TIME_LABELS.get(record_time, record_time),
                "status_text": status_text,
                "status_class": status_class,
                "status_url": status_url,
                "view_url": view_url,
            }
        )

    return render_template(
        "list_page.html",
        title="Cobas Pure Verification",
        items=items,
        date1=date1,
        date2=date2,
        timerec=timerec,
        show_time_filter=True,
        time_options=[
            ("onethirtyam", "1:30 AM"),
            ("eightam", "8 AM"),
            ("sevenpm", "7 PM"),
        ],
        pagination=pagination,
    )


@bp.route("/attalicaverification", methods=["GET", "POST"])
@login_required
def attalicaverification():
    rows, date1, date2, timerec, pagination = filtered_rows("attalica", "datetime", allow_time=True)
    view_endpoint_by_time = {
        "eightam": "main.view_attalica8am",
        "sevenpm": "main.view_attalica7pm",
        "twelvethirtyam": "main.view_attalica12am",
    }

    items = []
    row_start = pagination["start_index"] if pagination["start_index"] else 1
    for idx, row in enumerate(rows, start=row_start):
        status_text, status_class = status_meta(row.get("status", "0"))
        verify_enabled = str(row.get("status", "0")) != "1"
        record_time = str(row.get("timerec", ""))
        view_endpoint = view_endpoint_by_time.get(record_time)
        view_url = url_for(view_endpoint, id=row["id"]) if view_endpoint else ""

        if str(row.get("formfill", "0")) == "1":
            status_text = "Not Fill"
            status_class = "status-muted"
            verify_enabled = False
            view_url = ""

        items.append(
            {
                "id": row["id"],
                "sr": idx,
                "date": as_date_label(row.get("datetime")),
                "datetime": as_datetime_label(row.get("datetime")),
                "time": TIME_LABELS.get(str(row.get("timerec", "")), str(row.get("timerec", ""))),
                "status_text": status_text,
                "status_class": status_class,
                "status_url": "",
                "view_url": view_url,
                "verify_enabled": verify_enabled,
            }
        )

    return render_template(
        "list_page.html",
        title="Attalica Verification",
        items=items,
        date1=date1,
        date2=date2,
        timerec=timerec,
        show_time_filter=True,
        time_options=[
            ("eightam", "8 AM"),
            ("sevenpm", "7 PM"),
            ("twelvethirtyam", "12:30 AM"),
        ],
        attalica_mode=True,
        pagination=pagination,
    )


@bp.route("/aclelitemaint", methods=["GET", "POST"])
@login_required
def aclelitemaint():
    rows, date1, date2, timerec, pagination = filtered_rows("aclelite", "datetimess", allow_time=False)

    items = []
    row_start = pagination["start_index"] if pagination["start_index"] else 1
    for idx, row in enumerate(rows, start=row_start):
        status_text, status_class = status_meta(row.get("status", "0"))
        status_url = url_for("main.aclelitemainform", id=row["id"])
        view_url = url_for("main.view_aclelite", id=row["id"])

        if str(row.get("formfill", "0")) == "1":
            status_text = "Not Fill"
            status_class = "status-muted"
            status_url = ""
            view_url = ""

        items.append(
            {
                "id": row["id"],
                "sr": idx,
                "date": as_date_label(row.get("datetimess")),
                "datetime": as_datetime_label(row.get("datetimess")),
                "time": "8 AM",
                "status_text": status_text,
                "status_class": status_class,
                "status_url": status_url,
                "view_url": view_url,
            }
        )

    return render_template(
        "list_page.html",
        title="ACL Elite Verification",
        items=items,
        date1=date1,
        date2=date2,
        timerec=timerec,
        show_time_filter=False,
        pagination=pagination,
    )
