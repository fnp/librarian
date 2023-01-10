from .wers import Wers


class WersSrodek(Wers):
    TXT_PREFIX = '           '

    EPUB_ATTR = HTML_ATTR = {
        "style": "text-align: center",
    }
