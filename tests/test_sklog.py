"""
Tests for xlog. Run with: pytest
"""

import io
import pytest
from sklog import (
    xlog,
    xlog_error,
    xlog_warning,
    xlog_success,
    xlog_info,
    xlog_debug,
    xlog_header,
    xlog_separator,
    LogLevel,
)


def capture(fn, *args, **kwargs) -> str:
    """Helper: call fn with a StringIO file kwarg and return what it printed."""
    buf = io.StringIO()
    fn(*args, **kwargs, file=buf)
    return buf.getvalue()


class TestXlog:
    def test_default_flag_prints_message(self):
        out = capture(xlog, "hello world")
        assert "hello world" in out

    def test_known_flag_includes_symbol(self):
        out = capture(xlog, "test", "s")
        assert "[^]" in out

    def test_unknown_flag_falls_back_to_default(self):
        # Should not raise, should fall back to DEFAULT symbol.
        out = capture(xlog, "test", "z")
        assert "[ ]" in out

    def test_timestamp_appears_in_output(self):
        out = capture(xlog, "test", timestamp=True)
        # Timestamp format is HH:MM:SS - check the colons are present.
        assert ":" in out

    def test_bold_does_not_suppress_message(self):
        out = capture(xlog, "bold msg", "n", bold=True)
        assert "bold msg" in out

    def test_none_flag_is_same_as_default(self):
        out_none    = capture(xlog, "x", None)
        out_default = capture(xlog, "x")
        assert out_none == out_default


class TestWrappers:
    def test_xlog_warning(self):
        out = capture(xlog_warning, "watch out")
        assert "[!]" in out
        assert "watch out" in out

    def test_xlog_success(self):
        out = capture(xlog_success, "all good")
        assert "[^]" in out

    def test_xlog_info(self):
        out = capture(xlog_info, "just so you know")
        assert "[*]" in out

    def test_xlog_debug(self):
        out = capture(xlog_debug, "var=42")
        assert "[?]" in out

    def test_xlog_error_symbol(self):
        buf = io.StringIO()
        xlog_error("something broke", file=buf)
        assert "[#]" in buf.getvalue()

    def test_xlog_error_defaults_to_stderr(self):
        import sys, inspect
        sig = inspect.signature(xlog_error)
        assert sig.parameters["file"].default is sys.stderr


class TestHelpers:
    def test_header_contains_message(self):
        out = capture(xlog_header, "My Section")
        assert "My Section" in out

    def test_header_has_surrounding_newlines(self):
        out = capture(xlog_header, "Title")
        assert out.startswith("\n")
        assert out.endswith("\n\n")

    def test_separator_default_length(self):
        out = capture(xlog_separator)
        # Strip ANSI codes to count visible characters.
        visible = out.strip().replace("\033[96m", "").replace("\033[0m", "")
        assert len(visible) == 50

    def test_separator_custom_char_and_length(self):
        out = capture(xlog_separator, "-", 20)
        visible = out.strip().replace("\033[96m", "").replace("\033[0m", "")
        assert len(visible) == 20

    def test_separator_rejects_multi_char(self):
        with pytest.raises(ValueError):
            xlog_separator("--")

    def test_separator_rejects_empty_string(self):
        with pytest.raises(ValueError):
            xlog_separator("")


class TestLogLevel:
    def test_all_levels_have_unique_flags(self):
        flags = [l.flag for l in LogLevel if l.flag]
        assert len(flags) == len(set(flags))

    def test_property_accessors(self):
        assert LogLevel.SUCCESS.flag   == "s"
        assert LogLevel.SUCCESS.symbol == "[^]"
        assert LogLevel.ERROR.flag     == "e"
        assert LogLevel.ERROR.symbol   == "[#]"