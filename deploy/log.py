def _wrap_with(code):
    def inner(text, bold=False):
        c = code
        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)

    return inner


red = _wrap_with("31")
green = _wrap_with("32")
yellow = _wrap_with("33")
blue = _wrap_with("34")
magenta = _wrap_with("35")
cyan = _wrap_with("36")
white = _wrap_with("37")


def _format_text(text, before="\n", after="\n"):
    return f"{before}{text}{after}"


def warn(text, before="\n", after="\n"):
    print(yellow(_format_text(text, before=before, after=after)))


def error(text, before="\n", after="\n"):
    print(red(_format_text(text, before=before, after=after)))


def success(text, before="", after="\n"):
    print(green(_format_text(text, before=before, after=after)))


def info(text, before="", after=""):
    print(blue(_format_text(text, before=before, after=after)))


def debug(text, before="", after=""):
    print(cyan(_format_text(text, before=before, after=after)))


def section(text, space=True, separate=True, top="\n", bottom="\n"):
    if space:
        text = " %s " % text
    text = f"{text:=^80}"
    if separate:
        text = f"{top}{text}{bottom}"
    print(cyan(text))


def status(text, failed=False):
    if failed:
        return error(text + " - FAILED!")
    return success(text + " - DONE!")
