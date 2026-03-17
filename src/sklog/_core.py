"""
Internal implementation. Import from the top-level package, not here directly.
"""

from __future__ import annotations

import sys
from datetime import datetime
from enum import Enum
from typing import Optional, TextIO


class _Ansi:
    """Raw ANSI escape sequences. Not part of the public API."""

    RESET     = "\033[0m"
    BOLD      = "\033[1m"
    UNDERLINE = "\033[4m"
    RED       = "\033[91m"
    GREEN     = "\033[92m"
    YELLOW    = "\033[93m"
    BLUE      = "\033[94m"
    MAGENTA   = "\033[95m"
    CYAN      = "\033[96m"
    WHITE     = "\033[97m"


# Public alias so callers can do `from xlog import Colors`.
Colors = _Ansi


class LogLevel(Enum):
    """
    Each member carries (flag, color, symbol) so a single lookup gives
    everything needed to render a line.
    """

    DEBUG   = ("d", _Ansi.MAGENTA, "[?]")
    ERROR   = ("e", _Ansi.RED,     "[#]")
    WARNING = ("w", _Ansi.YELLOW,  "[!]")
    SUCCESS = ("s", _Ansi.GREEN,   "[^]")
    INFO    = ("n", _Ansi.BLUE,    "[*]")
    DEFAULT = ("",  _Ansi.WHITE,   "[ ]")

    @property
    def flag(self) -> str:
        return self.value[0]

    @property
    def color(self) -> str:
        return self.value[1]

    @property
    def symbol(self) -> str:
        return self.value[2]


# Built once at import time rather than rebuilt on every xlog() call.
_FLAG_MAP: dict[str, LogLevel] = {
    level.flag: level
    for level in LogLevel
    if level.flag
}


def xlog(
    msg: str,
    flag: Optional[str] = None,
    *,
    timestamp: bool = False,
    bold: bool = False,
    file: TextIO = sys.stdout,
) -> None:
    """
    Print a colored, optionally timestamped log line.

    Args:
        msg:       The text to display.
        flag:      Severity shorthand - 'd', 'e', 'w', 's', or 'n'.
                   Omit (or pass None) for the unstyled default.
        timestamp: Prepend HH:MM:SS when True.
        bold:      Apply bold styling to both symbol and message when True.
        file:      Output stream. Defaults to stdout.

    Unknown flags fall back to DEFAULT silently rather than raising.
    """
    level = _FLAG_MAP.get(flag or "", LogLevel.DEFAULT)

    symbol_part = (
        f"{_Ansi.BOLD}{level.color}{level.symbol}{_Ansi.RESET}"
        if bold else
        f"{level.color}{level.symbol}{_Ansi.RESET}"
    )

    if timestamp:
        ts = datetime.now().strftime("%H:%M:%S")
        symbol_part = f"{level.color}[{ts}]{_Ansi.RESET} {symbol_part}"

    msg_part = (
        f"{_Ansi.BOLD}{level.color}{msg}{_Ansi.RESET}"
        if bold else
        f"{level.color}{msg}{_Ansi.RESET}"
    )

    print(f"{symbol_part} {msg_part}", file=file)


def xlog_error(msg: str, *, timestamp: bool = False, file: TextIO = sys.stderr) -> None:
    """Log an error. Defaults to stderr so it separates cleanly from stdout."""
    xlog(msg, "e", timestamp=timestamp, file=file)


def xlog_warning(msg: str, *, timestamp: bool = False, file: TextIO = sys.stdout) -> None:
    """Log a warning."""
    xlog(msg, "w", timestamp=timestamp, file=file)


def xlog_success(msg: str, *, timestamp: bool = False, file: TextIO = sys.stdout) -> None:
    """Log a success confirmation."""
    xlog(msg, "s", timestamp=timestamp, file=file)


def xlog_info(msg: str, *, timestamp: bool = False, file: TextIO = sys.stdout) -> None:
    """Log general information."""
    xlog(msg, "n", timestamp=timestamp, file=file)


def xlog_debug(msg: str, *, timestamp: bool = False, file: TextIO = sys.stdout) -> None:
    """Log a debug detail. Gate behind an env flag in production if needed."""
    xlog(msg, "d", timestamp=timestamp, file=file)


def xlog_header(msg: str, *, file: TextIO = sys.stdout) -> None:
    """Print a bold, underlined section header surrounded by blank lines."""
    print(f"\n{_Ansi.BOLD}{_Ansi.UNDERLINE}{msg}{_Ansi.RESET}\n", file=file)


def xlog_separator(char: str = "=", length: int = 50, *, file: TextIO = sys.stdout) -> None:
    """
    Print a horizontal rule.

    Args:
        char:   Single character to repeat. Defaults to '='.
        length: Total width. Defaults to 50.

    Raises:
        ValueError: If char is not exactly one character.
    """
    if len(char) != 1:
        raise ValueError(f"separator char must be a single character, got {char!r}")
    print(f"{_Ansi.CYAN}{char * length}{_Ansi.RESET}", file=file)
