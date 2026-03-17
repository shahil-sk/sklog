"""
sklog - Lightweight colored console logging for Python.

Basic usage::

    from sklog import xlog_info, xlog_error, xlog_success

    xlog_info("Server started")
    xlog_error("Connection refused")
    xlog_success("Build passed", timestamp=True)

Or use the generic entry point with a flag::

    from sklog import xlog

    xlog("Retrying...", "w")
    xlog("Done", "s", bold=True)
"""

from sklog._core import (
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