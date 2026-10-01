from .web.blueprint import bp
from .web import auth_routes, dashboard_routes, form_routes, sample_discard_routes, verification_routes, view_routes

__all__ = [
    "bp",
    "auth_routes",
    "dashboard_routes",
    "form_routes",
    "sample_discard_routes",
    "verification_routes",
    "view_routes",
]
