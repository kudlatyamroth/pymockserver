from typing import Callable


def _wrap_with(code: str) -> Callable[[str], str]:
    def inner(text: str) -> str:
        c = code
        return "\033[%sm%s\033[0m" % (c, text)

    return inner


def _wrap_bold_with(code: str) -> Callable[[str], str]:
    def inner(text: str) -> str:
        c = "1;%s" % code
        return "\033[%sm%s\033[0m" % (c, text)

    return inner


red = _wrap_with("31")
green = _wrap_with("32")
yellow = _wrap_with("33")
blue = _wrap_with("34")
magenta = _wrap_with("35")
cyan = _wrap_with("36")
white = _wrap_with("37")

red_bold = _wrap_bold_with("31")
green_bold = _wrap_bold_with("32")
yellow_bold = _wrap_bold_with("33")
blue_bold = _wrap_bold_with("34")
magenta_bold = _wrap_bold_with("35")
cyan_bold = _wrap_bold_with("36")
white_bold = _wrap_bold_with("37")


def _format_text(text: str, before: str = "\n", after: str = "\n") -> str:
    return f"{before}{text}{after}"


def warn(text: str, before: str = "\n", after: str = "\n") -> None:
    print(yellow(_format_text(text, before=before, after=after)))


def error(text: str, before: str = "\n", after: str = "\n") -> None:
    print(red(_format_text(text, before=before, after=after)))


def success(text: str, before: str = "", after: str = "\n") -> None:
    print(green(_format_text(text, before=before, after=after)))


def info(text: str, before: str = "", after: str = "") -> None:
    print(blue(_format_text(text, before=before, after=after)))


def debug(text: str, before: str = "", after: str = "") -> None:
    print(cyan(_format_text(text, before=before, after=after)))


def section(text: str, space: bool = True, separate: bool = True, top: str = "\n", bottom: str = "\n") -> None:
    if space:
        text = " %s " % text
    text = f"{text:=^80}"
    if separate:
        text = f"{top}{text}{bottom}"
    print(cyan(text))


def status(text: str, failed: bool = False) -> None:
    if failed:
        return error(f"{text} - FAILED!")
    return success(f"{text} - DONE!")
