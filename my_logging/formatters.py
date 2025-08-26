import json
import logging
import re

_ANSI_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")

class PlainFormatter(logging.Formatter):
    """Plain text. Strips any stray ANSI codes from message."""
    def format(self, record):
        s = super().format(record)
        return _ANSI_RE.sub("", s)

class JsonFormatter(logging.Formatter):
    """Line-oriented JSON for file logs."""
    def format(self, record):
        payload = {
            "ts": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "file": record.filename,
            "line": record.lineno,
            "func": record.funcName,
            "user_id": getattr(record, "user_id", None),
            "user_name": getattr(record, "user_name", None),
        }
        return json.dumps(payload, ensure_ascii=False)
