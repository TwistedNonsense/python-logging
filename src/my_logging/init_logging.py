import logging
import os
from logging.handlers import RotatingFileHandler
from .config import DEFAULTS as C
from .filters import FlaskUserFilter
from .formatters import PlainFormatter, JsonFormatter

NOISY_LIBS = ["werkzeug", "sqlalchemy.engine", "socketio", "engineio"]

def silence_noisy_libs(level=logging.WARNING):
    for name in NOISY_LIBS:
        logging.getLogger(name).setLevel(level)

def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def _to_level(val, default):
    if isinstance(val, int):
        return val
    try:
        return getattr(logging, str(val).upper())
    except Exception:
        return default

def init_logging(
    *, app=None,
    log_dir=None, log_file=None,
    level=None, console_level=None, file_level=None,
    max_bytes=None, backup_count=None,
    console_fmt=None, file_fmt=None,
    json_file=None
):
    """Initialize logging for Flask or plain Python apps.
    Returns the configured logger (app.logger if app provided, else root).
    """
    log_dir = log_dir or C["LOG_DIR"]
    log_file = log_file or C["LOG_FILE"]
    level = _to_level(level or C["LEVEL"], logging.INFO)
    console_level = _to_level(console_level or C["CONSOLE_LEVEL"], logging.DEBUG)
    file_level = _to_level(file_level or C["FILE_LEVEL"], logging.INFO)
    max_bytes = max_bytes or C["MAX_BYTES"]
    backup_count = backup_count or C["BACKUP_COUNT"]
    console_fmt = console_fmt or C["FORMAT_CONSOLE"]
    file_fmt = file_fmt or C["FORMAT_FILE"]
    json_file = C["JSON_FILE"] if json_file is None else bool(json_file)

    _ensure_dir(log_dir)
    logfile_path = os.path.join(log_dir, log_file)

    if app is not None:
        logger = app.logger
    else:
        logger = logging.getLogger()

    # Reset handlers to avoid duplicates
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(level)

    # Console
    ch = logging.StreamHandler()
    ch.setLevel(console_level)
    ch.setFormatter(PlainFormatter(console_fmt))
    ch.addFilter(FlaskUserFilter())
    logger.addHandler(ch)

    # File
    fh = RotatingFileHandler(logfile_path, maxBytes=max_bytes, backupCount=backup_count)
    fh.setLevel(file_level)
    fh.setFormatter(JsonFormatter() if json_file else PlainFormatter(file_fmt))
    fh.addFilter(FlaskUserFilter())
    logger.addHandler(fh)

    silence_noisy_libs()

    if app is not None:
        logging.getLogger().setLevel(logging.ERROR)

    return logger
