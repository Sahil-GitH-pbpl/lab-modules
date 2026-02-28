from functools import wraps

from flask import Blueprint, redirect, session, url_for

from ..forms_config import NAV_ITEMS

bp = Blueprint("main", __name__)


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("userid"):
            return redirect(url_for("main.login"))
        return fn(*args, **kwargs)

    return wrapper


@bp.app_context_processor
def inject_layout_globals():
    return {
        "nav_items": NAV_ITEMS,
        "current_user": session.get("empname", ""),
    }
