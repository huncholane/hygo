import logging
import re


class TermEscapeCodeFormatter(logging.Formatter):
    """A class to strip the escape codes from the """

    def __init__(self, fmt=None, datefmt=None, style='%', validate=True):
        super().__init__(fmt, datefmt, style, validate)

    def format(self, record):
        escape_re = re.compile(r'\x1b\[[0-9;]*m')
        record.msg = re.sub(escape_re, "", str(record.msg))
        s = super().format(record)
        if record.exc_text:
            s = s.splitlines()[0][:-10]
            exc = record.exc_text.replace('\n', '<br>')
            s = s+'<br><br>'+exc+'</td></tr>'
        return s
