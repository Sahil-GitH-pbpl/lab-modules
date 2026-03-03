from datetime import datetime

from flask import render_template, request, url_for

from ..db import fetch_all
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


@bp.route("/mindraybc700verification", methods=["GET"])
@login_required
def mindraybc700verification():
    rows, date1, date2, timerec, pagination = filtered_rows("mindraybc700", "datetime", allow_time=True)
    view_endpoint_by_time = {
        "eightam": "main.view_mindraybc7008am",
    }

    items = []
    row_start = pagination["start_index"] if pagination["start_index"] else 1
    for idx, row in enumerate(rows, start=row_start):
        status_text, status_class = status_meta(row.get("status", "0"))
        record_time = str(row.get("timerec", ""))
        view_endpoint = view_endpoint_by_time.get(record_time)
        view_url = url_for(view_endpoint, id=row["id"]) if view_endpoint else ""
        status_url = url_for("main.mindraybc700mainform", id=row["id"])

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
        title="Mindray BC 700 Verification",
        items=items,
        date1=date1,
        date2=date2,
        timerec=timerec,
        show_time_filter=True,
        time_options=[
            ("eightam", "8 AM"),
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


@bp.route("/lifotronicverification", methods=["GET", "POST"])
@login_required
def lifotronicverification():
    date1 = (request.values.get("date1") or "").strip()
    date2 = (request.values.get("date2") or "").strip()
    timerec = (request.values.get("timerec") or "").strip().lower()
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
    params: list[str] = []
    if date1 and date2:
        where.append("DATE(created_at) BETWEEN %s AND %s")
        params.extend([date1, date2])

    where_sql = ""
    if where:
        where_sql = " WHERE " + " AND ".join(where)

    records = []
    if timerec in ("", "daily"):
        daily_rows = fetch_all(
            f"SELECT id, created_at, status FROM lifotronic_h100_daily{where_sql}",
            tuple(params),
        )
        for row in daily_rows:
            records.append(
                {
                    "id": row.get("id"),
                    "created_at": row.get("created_at"),
                    "status": row.get("status", "0"),
                    "form_type": "daily",
                }
            )

    if timerec in ("", "weekly"):
        weekly_rows = fetch_all(
            f"SELECT id, created_at, status FROM lifotronic_h100_weekly{where_sql}",
            tuple(params),
        )
        for row in weekly_rows:
            records.append(
                {
                    "id": row.get("id"),
                    "created_at": row.get("created_at"),
                    "status": row.get("status", "0"),
                    "form_type": "weekly",
                }
            )

    def sort_key(item: dict):
        value = item.get("created_at")
        if isinstance(value, datetime):
            return value
        raw = str(value or "").strip()
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %I:%M %p", "%Y-%m-%d"):
            try:
                return datetime.strptime(raw, fmt)
            except ValueError:
                continue
        return datetime.min

    records.sort(key=sort_key, reverse=True)
    total_records = len(records)

    if is_all:
        per_page = total_records if total_records > 0 else 1
        total_pages = 1
        page = 1
    else:
        total_pages = max((total_records + per_page - 1) // per_page, 1)
        if page > total_pages:
            page = total_pages

    offset = (page - 1) * per_page
    page_rows = records[offset : offset + per_page]
    if total_records:
        start_index = offset + 1
        end_index = min(offset + len(page_rows), total_records)
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

    items = []
    row_start = start_index if start_index else 1
    for idx, row in enumerate(page_rows, start=row_start):
        status_text, status_class = status_meta(row.get("status", "0"))
        is_weekly = row.get("form_type") == "weekly"
        status_url = url_for(
            "main.lifotronicweeklymainform" if is_weekly else "main.lifotronicmainform",
            id=row["id"],
        )
        view_url = url_for(
            "main.view_lifotronic_weekly" if is_weekly else "main.view_lifotronic_daily",
            id=row["id"],
        )
        items.append(
            {
                "id": row["id"],
                "sr": idx,
                "date": as_date_label(row.get("created_at")),
                "datetime": as_datetime_label(row.get("created_at")),
                "time": "Weekly" if is_weekly else "Daily",
                "status_text": status_text,
                "status_class": status_class,
                "status_url": status_url,
                "view_url": view_url,
            }
        )

    return render_template(
        "list_page.html",
        title="LIFOTRONIC H100 Verification",
        items=items,
        date1=date1,
        date2=date2,
        timerec=timerec,
        show_time_filter=True,
        time_options=[
            ("daily", "Daily Form"),
            ("weekly", "Weekly Form"),
        ],
        pagination=pagination,
    )


@bp.route("/laurav2verification", methods=["GET"])
@login_required
def laurav2_verification():
    date1 = (request.values.get("date1") or "").strip()
    date2 = (request.values.get("date2") or "").strip()
    timerec = (request.values.get("timerec") or "").strip().lower()
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
    params: list[str] = []
    if date1 and date2:
        where.append("DATE(created_at) BETWEEN %s AND %s")
        params.extend([date1, date2])

    where_sql = ""
    if where:
        where_sql = " WHERE " + " AND ".join(where)

    records = []
    if timerec in ("", "daily"):
        daily_rows = fetch_all(
            f"SELECT id, created_at, status FROM laurav2_daily{where_sql}",
            tuple(params),
        )
        for row in daily_rows:
            records.append(
                {
                    "id": row.get("id"),
                    "created_at": row.get("created_at"),
                    "status": row.get("status", "0"),
                    "form_type": "daily",
                }
            )

    if timerec in ("", "weekly"):
        weekly_rows = fetch_all(
            f"SELECT id, created_at, status FROM laurav2_weekly{where_sql}",
            tuple(params),
        )
        for row in weekly_rows:
            records.append(
                {
                    "id": row.get("id"),
                    "created_at": row.get("created_at"),
                    "status": row.get("status", "0"),
                    "form_type": "weekly",
                }
            )

    def sort_key(item: dict):
        value = item.get("created_at")
        if isinstance(value, datetime):
            return value
        raw = str(value or "").strip()
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %I:%M %p", "%Y-%m-%d"):
            try:
                return datetime.strptime(raw, fmt)
            except ValueError:
                continue
        return datetime.min

    records.sort(key=sort_key, reverse=True)
    total_records = len(records)

    if is_all:
        per_page = total_records if total_records > 0 else 1
        total_pages = 1
        page = 1
    else:
        total_pages = max((total_records + per_page - 1) // per_page, 1)
        if page > total_pages:
            page = total_pages

    offset = (page - 1) * per_page
    page_rows = records[offset : offset + per_page]
    if total_records:
        start_index = offset + 1
        end_index = min(offset + len(page_rows), total_records)
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

    items = []
    row_start = start_index if start_index else 1
    for idx, row in enumerate(page_rows, start=row_start):
        status_text, status_class = status_meta(row.get("status", "0"))
        is_weekly = row.get("form_type") == "weekly"
        status_url = url_for(
            "main.laurav2weeklymainform" if is_weekly else "main.laurav2dailymainform",
            id=row["id"],
        )
        view_url = url_for(
            "main.view_laurav2_weekly" if is_weekly else "main.view_laurav2_daily",
            id=row["id"],
        )
        items.append(
            {
                "id": row["id"],
                "sr": idx,
                "date": as_date_label(row.get("created_at")),
                "datetime": as_datetime_label(row.get("created_at")),
                "time": "Weekly" if is_weekly else "Daily",
                "status_text": status_text,
                "status_class": status_class,
                "status_url": status_url,
                "view_url": view_url,
            }
        )

    return render_template(
        "list_page.html",
        title="LAURA V2 Verification",
        items=items,
        date1=date1,
        date2=date2,
        timerec=timerec,
        show_time_filter=True,
        time_options=[
            ("daily", "Daily Form"),
            ("weekly", "Weekly Form"),
        ],
        pagination=pagination,
    )
