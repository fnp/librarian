from .wers import Wers


class WersDoPrawej(Wers):
    TXT_PREFIX = '                       '

    HTML_ATTR = {
        "style": "text-align: right",
    }
