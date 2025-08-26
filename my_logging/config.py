import os

DEFAULTS = {
    "LOG_DIR": os.getenv("LOG_DIR", "logs"),
    "LOG_FILE": os.getenv("LOG_FILE", "app.log"),
    "LEVEL": os.getenv("LOG_LEVEL", "INFO"),
    "CONSOLE_LEVEL": os.getenv("LOG_CONSOLE_LEVEL", "DEBUG"),
    "FILE_LEVEL": os.getenv("LOG_FILE_LEVEL", "INFO"),
    "MAX_BYTES": int(os.getenv("LOG_MAX_BYTES", str(5 * 1024 * 1024))),  # 5 MB
    "BACKUP_COUNT": int(os.getenv("LOG_BACKUP_COUNT", "20")),
    "FORMAT_CONSOLE": os.getenv(
        "LOG_FORMAT_CONSOLE",
        "%(asctime)s %(levelname)s in %(module)s [%(funcName)s]: %(message)s",
    ),
    "FORMAT_FILE": os.getenv(
        "LOG_FORMAT_FILE",
        "%(asctime)s %(levelname)s in %(filename)s:%(lineno)d [%(funcName)s]: %(message)s",
    ),
    "JSON_FILE": os.getenv("LOG_JSON_FILE", "0") in {"1", "true", "True"},
}
