# Logging kit

_Drop-in logging for Python and Flask projects. No colors. Rotating file + console. Optional JSON file output. Safe in or out of Flask context._

For projects where I want logs formatted like this: 
```
2023-03-26 11:42:29,661 INFO in auth_routes.py:93 [login]: Attempting login for username 'superadmin1'
2023-03-26 11:42:29,981 INFO in auth_routes.py:98 [login]: Password correct for user ID '671'
2023-03-26 11:42:30,151 INFO in dashboard_routes.py:31 [dashboard]: Super Admin 1 (671) accessed the dashboard
2023-03-26 11:43:14,388 INFO in rbac.py:57 [perm_req]: Checking permissions for Super Admin 1 (671)
2023-03-26 11:43:14,388 INFO in rbac.py:66 [perm_req]: Permission 'user_view_all' is required
2023-03-26 11:43:14,475 INFO in rbac.py:87 [perm_req]: Access Granted. Super Admin 1 (671) has permission 'user_view_all'
2023-03-26 11:43:14,475 INFO in user_routes.py:24 [users]: Super Admin 1 (671) viewed the users list page
```

With `logging_helpers.py` I simplify the process so I can add log statements like this: 
```
log_info("Attempting login for username '%s'", username)
log_warning("Failed login attempt for %s", username)
log_error("Some error happened...")
```

## Structure (in root)
```
my_logging/
  __init__.py
  config.py
  filters.py
  formatters.py
  init_logging.py
utils/
  logging_helpers.py   # provides log_info/log_warning/log_error/log_critical
```

## Quick start (plain Python)
```python
from my_logging import init_logging
from utils.logging_helpers import log_info, log_error

logger = init_logging()   # creates logs/app.log
log_info("service started")
log_error("example problem")
```

## Quick start (Flask)
```python
from flask import Flask
from my_logging import init_logging
from utils.logging_helpers import log_info

def create_app():
    app = Flask(__name__)
    init_logging(app=app)
    @app.route("/")
    def ping():
        log_info("ping")
        return "ok"
    return app
```

## Env vars (optional)
```
LOG_DIR=logs
LOG_FILE=app.log
LOG_LEVEL=INFO
LOG_CONSOLE_LEVEL=DEBUG
LOG_FILE_LEVEL=INFO
LOG_MAX_BYTES=5242880
LOG_BACKUP_COUNT=20
LOG_FORMAT_CONSOLE="%(asctime)s %(levelname)s in %(module)s [%(funcName)s]: %(message)s"
LOG_FORMAT_FILE="%(asctime)s %(levelname)s in %(filename)s:%(lineno)d [%(funcName)s]: %(message)s"
LOG_JSON_FILE=0   # 1 enables JSON lines for file handler
```

## Notes
- Handlers are reset on init to avoid duplicates.
- `utils.logging_helpers` picks Flask `current_app.logger` when available, else falls back to root logger, so the same `log_info(...)` calls work in both contexts.
- ANSI stripping is in the formatter to prevent stray codes from reaching files.
- `silence_noisy_libs()` reduces chatter from Werkzeug, SQLAlchemy engine, Socket.IO, and Engine.IO. Adjust as needed.
