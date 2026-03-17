# xlog

Lightweight colored console logging for Python. No dependencies, just stdlib.

```
pip install xlog
```

---

## Quick start

```python
from xlog import xlog_info, xlog_warning, xlog_error, xlog_success, xlog_debug

xlog_info("Server started on port 8080")
xlog_warning("Disk usage above 80 percent")
xlog_error("Database connection refused")
xlog_success("Deployment finished")
xlog_debug("Cache miss for key user:42")
```

Output (colored in terminal):

```
[*] Server started on port 8080
[!] Disk usage above 80 percent
[#] Database connection refused
[^] Deployment finished
[?] Cache miss for key user:42
```

---

## API reference

### Generic function

```python
xlog(msg, flag=None, *, timestamp=False, bold=False, file=sys.stdout)
```

| flag | level   | color   |
|------|---------|---------|
| `"d"` | DEBUG  | magenta |
| `"e"` | ERROR  | red     |
| `"w"` | WARNING | yellow |
| `"s"` | SUCCESS | green  |
| `"n"` | INFO   | blue    |
| `None` | DEFAULT | white |

### Typed wrappers

```python
xlog_debug(msg, *, timestamp=False)
xlog_info(msg, *, timestamp=False)
xlog_warning(msg, *, timestamp=False)
xlog_error(msg, *, timestamp=False)   # writes to stderr
xlog_success(msg, *, timestamp=False)
```

### Formatting helpers

```python
xlog_header("Section Title")           # bold + underlined, surrounded by blank lines
xlog_separator(char="=", length=50)    # horizontal rule in cyan
```

### Options

**`timestamp=True`** — prepends `HH:MM:SS` to the line:

```python
xlog_success("Build passed", timestamp=True)
# [14:32:07] [^] Build passed
```

**`bold=True`** — makes both the symbol and message bold:

```python
xlog("Critical path completed", "s", bold=True)
```

---

## Install for development

```bash
git clone https://github.com/shahil-sk/xlog
cd xlog
pip install -e ".[dev]"
pytest
```

---

## License

MIT
