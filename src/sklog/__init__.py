"""
xlog - Lightweight colored console logging for Python.

Basic usage::

    from xlog import xlog_info, xlog_error, xlog_success

    xlog_info("Server started")
    xlog_error("Connection refused")
    xlog_success("Build passed", timestamp=True)

Or use the generic entry point with a flag::

    from xlog import xlog

    xlog("Retrying...", "w")
    xlog("Done", "s", bold=True)
"""

from xlog._core import (
    Colors,
    LogLevel,
    xlog,
    xlog_debug,
    xlog_error,
    xlog_header,
    xlog_info,
    xlog_separator,
    xlog_success,
    xlog_warning,
)

__version__ = "2.0.0"
__author__  = "shahil-sk"

__all__ = [
    "Colors",
    "LogLevel",
    "xlog",
    "xlog_debug",
    "xlog_error",
    "xlog_header",
    "xlog_info",
    "xlog_separator",
    "xlog_success",
    "xlog_warning",
]
