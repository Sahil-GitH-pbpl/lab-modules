from datetime import datetime
import re
from zoneinfo import ZoneInfo

from flask import flash, redirect, render_template, request, session

from ..db import execute, fetch_all
from .blueprint import bp, login_required
from .helpers import as_datetime_label

DEPARTMENT_OPTIONS = (
    "Hematology-Biochemistry",
    "Microbiology",
    "Histopathology",
    "Molecular",
)

DEFAULT_DEPARTMENT = "Hematology-Biochemistry"
ROW_LIMIT_OPTIONS = ("20", "50", "100", "all")


def _parse_sample_tokens(raw_input: str) -> list[str]:
    raw = (raw_input or "").strip()
    if not raw:
        return []

    barcode_pattern = re.compile(r"\d+-\d")
    concatenated_barcode_pattern = re.compile(r"\d+?-\d(?=\d|$)")
    tokens: list[str] = []

    # First split by normal separators, then split scanner-concatenated chunks.
    chunks = [part.strip() for part in re.split(r"[\s,;\n\r\t]+", raw.replace(",", " ")) if part.strip()]
    for chunk in chunks:
        if barcode_pattern.fullmatch(chunk):
            tokens.append(chunk)
            continue

        matches = concatenated_barcode_pattern.findall(chunk)
        if matches and "".join(matches) == chunk:
            tokens.extend(matches)
            continue

        tokens.append(chunk)

    return tokens


def _build_sample_preview(sample_ids: str, visible_count: int = 40) -> tuple[str, str, bool]:
    tokens = [part.strip() for part in (sample_ids or "").split(",") if part.strip()]
    preview = ", ".join(tokens[:visible_count])
    remaining = ", ".join(tokens[visible_count:])
    return preview, remaining, len(tokens) > visible_count


def _backfill_missing_departments() -> None:
    execute(
        "UPDATE sample_discard SET department = %s WHERE department IS NULL OR TRIM(department) = ''",
        (DEFAULT_DEPARTMENT,),
    )


@bp.route("/sample-discard-form", methods=["GET", "POST"])
@login_required
def sample_discard_form():
    _backfill_missing_departments()

    if request.method == "POST":
        department = (request.form.get("department") or "").strip()
        if department not in DEPARTMENT_OPTIONS:
            flash("Please select a department.", "error")
            return redirect(request.path)

        raw_input = (request.form.get("sample_ids") or "").strip()
        if not raw_input:
            flash("Please enter at least one sample ID.", "error")
            return redirect(request.path)

        tokens = _parse_sample_tokens(raw_input)
        if not tokens:
            flash("Please enter at least one valid sample ID.", "error")
            return redirect(request.path)

        sample_ids = ", ".join(tokens)
        discarded_by = (session.get("empname") or "").strip()
        discarded_at = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")

        execute(
            "INSERT INTO sample_discard (department, sample_ids, discarded_by, discarded_at) VALUES (%s, %s, %s, %s)",
            (department, sample_ids, discarded_by, discarded_at),
        )
        flash("Sample discard entry saved successfully.", "success")
        return redirect(request.path)

    return render_template(
        "sample_discard_form.html",
        title="Sample Discard",
        panel_subtitle="Scan and enter sample IDs.",
        department_options=DEPARTMENT_OPTIONS,
        selected_department="",
    )


@bp.route("/sample-discard-list", methods=["GET"])
@login_required
def sample_discard_list():
    _backfill_missing_departments()

    # Department filter is temporarily disabled for the discard sample list.
    # department = (request.args.get("department") or "").strip()
    # selected_department = department if department in DEPARTMENT_OPTIONS else ""
    selected_department = ""

    row_limit = (request.args.get("rows") or "20").strip().lower()
    selected_rows = row_limit if row_limit in ROW_LIMIT_OPTIONS else "20"

    sql = "SELECT id, department, sample_ids, discarded_at FROM sample_discard"
    params: list[str | int] = []

    # if selected_department:
    #     sql += " WHERE department = %s"
    #     params.append(selected_department)

    sql += " ORDER BY discarded_at DESC, id DESC"

    if selected_rows != "all":
        sql += " LIMIT %s"
        params.append(int(selected_rows))

    rows = fetch_all(sql, tuple(params))
    items = []
    for idx, row in enumerate(rows, start=1):
        preview_ids, remaining_ids, has_more = _build_sample_preview(row.get("sample_ids", ""))
        items.append(
            {
                "sr": idx,
                "department": row.get("department", ""),
                "sample_ids_preview": preview_ids,
                "sample_ids_remaining": remaining_ids,
                "sample_ids_has_more": has_more,
                "discarded_at": as_datetime_label(row.get("discarded_at")),
            }
        )

    return render_template(
        "sample_discard_list.html",
        title="All Discard Samples",
        items=items,
        department_options=DEPARTMENT_OPTIONS,
        selected_department=selected_department,
        row_limit_options=ROW_LIMIT_OPTIONS,
        selected_rows=selected_rows,
    )
