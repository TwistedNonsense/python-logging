import logging

class FlaskUserFilter(logging.Filter):
    """Injects user/session info if Flask context exists. Safe otherwise."""
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            from flask import has_request_context, session
            from flask_login import current_user
            if has_request_context():
                record.user_id = getattr(current_user, "id", None) or session.get("user_id") or "-"
                record.user_name = getattr(current_user, "name", None) or session.get("user_name") or "-"
            else:
                record.user_id = "-"
                record.user_name = "-"
        except Exception:
            record.user_id = "-"
            record.user_name = "-"
        return True
