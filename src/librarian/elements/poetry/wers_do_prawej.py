from .wers import Wers


class WersDoPrawej(Wers):
    TXT_PREFIX = '                       '

    EPUB_ATTR = HTML_ATTR = {
        "style": "text-align: right",
    }
