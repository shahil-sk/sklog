# sklog

Lightweight colored console logging for Python. Zero dependencies, pure stdlib.

```bash
pip install sklog
```

---

## Why sklog

Python's built-in `logging` module is powerful but verbose to configure for
simple scripts and CLI tools. `xlog` gives you colored, leveled output in one
import with no setup.

---

## Quick start

```python
from sklog import xlog_info, xlog_warning, xlog_error, xlog_success, xlog_debug

xlog_info("Server started on port 8080")
xlog_warning("Disk usage above 80 percent")
xlog_error("Database connection refused")
xlog_success("Deployment finished")
xlog_debug("Cache miss for key user:42")
```

Terminal output:

```python
[*] Server started on port 8080
[!] Disk usage above 80 percent
[#] Database connection refused
[^] Deployment finished
[?] Cache miss for key user:42
```

Each level prints in its own color — blue, yellow, red, green, magenta.

---

## All functions

### Typed wrappers

The easiest way to log. Each function maps to a fixed level.

```python
xlog_info("Listening on port 8080")         # blue    [*]
xlog_warning("Retrying in 5 seconds")       # yellow  [!]
xlog_error("Permission denied")             # red     [#]  → writes to stderr
xlog_success("All tests passed")            # green   [^]
xlog_debug("payload = {'id': 42}")          # magenta [?]
```

All wrappers accept two keyword arguments:

```python
xlog_success("Deployed", timestamp=True)    # prepend HH:MM:SS
xlog_error("Crashed", timestamp=True)
```

### Generic function

When you want to pick the level dynamically:

```python
from sklog import xlog

xlog("Starting up")              # default, white
xlog("Watch this", "w")         # warning
xlog("Done", "s", bold=True)    # success, bold
xlog("Trace", "d", timestamp=True, bold=True)
```

Full signature:

```python
xlog(msg, flag=None, *, timestamp=False, bold=False, file=sys.stdout)
```

| flag   | level   | color   | symbol |
|--------|---------|---------|--------|
| `"d"`  | DEBUG   | magenta | `[?]`  |
| `"e"`  | ERROR   | red     | `[#]`  |
| `"w"`  | WARNING | yellow  | `[!]`  |
| `"s"`  | SUCCESS | green   | `[^]`  |
| `"n"`  | INFO    | blue    | `[*]`  |
| `None` | DEFAULT | white   | `[ ]`  |

Unknown flags fall back to DEFAULT silently rather than raising.

### Formatting helpers

```python
from sklog import xlog_header, xlog_separator

xlog_header("Build Report")          # bold + underlined, blank lines above and below
xlog_separator()                     # cyan === line, 50 chars wide
xlog_separator("-", 30)             # custom char and width
```

---

## Options

### `timestamp=True`

Prepends the current time in `HH:MM:SS` format:

```python
xlog_success("Build passed", timestamp=True)
# [14:32:07] [^] Build passed

xlog_error("Timeout", timestamp=True)
# [14:32:09] [#] Timeout
```

### `bold=True`

Makes the symbol and message text bold. Only available on `xlog` directly:

```python
xlog("Critical section complete", "s", bold=True)
```

### `file=`

Redirect output to any writable stream. Useful in tests or when writing logs
to a file alongside printing:

```python
import sys
xlog_warning("Low memory", file=sys.stderr)

with open("run.log", "w") as f:
    xlog_info("Started", file=f)
```

`xlog_error` defaults to `sys.stderr`. All other functions default to `sys.stdout`.

---

## Real-world example

```python
from sklog import xlog_header, xlog_info, xlog_success, xlog_error, xlog_separator

def deploy(service: str) -> None:
    xlog_header(f"Deploying {service}")

    xlog_info("Pulling latest image", timestamp=True)
    xlog_info("Running migrations", timestamp=True)

    ok = run_migrations()

    if ok:
        xlog_success("Migrations applied", timestamp=True)
        xlog_success(f"{service} is live")
    else:
        xlog_error("Migration failed — rolling back", timestamp=True)

    xlog_separator()
```

Output:

```

Deploying api-service

[14:05:01] [*] Pulling latest image
[14:05:02] [*] Running migrations
[14:05:04] [^] Migrations applied
[^] api-service is live
==================================================
```

---

## Requirements

- Python 3.8 or newer
- No third-party dependencies

---

## Development

```bash
git clone https://github.com/shahil-sk/sklog
cd sklog
pip install -e ".[dev]"
pytest -v
```

---

## License

MIT — see [LICENSE](LICENSE).