"""Thin, color-free helpers for consistent call sites across projects."""
import logging

def _get_logger():
    # Prefer Flask app logger if available
    try:
        from flask import current_app
        if current_app:  # will raise RuntimeError if no app context
            return current_app.logger
    except Exception:
        pass
    # Fallback to module logger
    return logging.getLogger()

def log_debug(message, *args, **kwargs):
    _get_logger().debug(message, *args, stacklevel=2, **kwargs)

def log_info(message, *args, **kwargs):
    _get_logger().info(message, *args, stacklevel=2, **kwargs)

def log_warning(message, *args, **kwargs):
    _get_logger().warning(message, *args, stacklevel=2, **kwargs)

def log_error(message, *args, **kwargs):
    _get_logger().error(message, *args, stacklevel=2, **kwargs)

def log_critical(message, *args, **kwargs):
    _get_logger().critical(message, *args, stacklevel=2, **kwargs)
