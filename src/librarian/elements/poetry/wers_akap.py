from .wers import Wers


class WersAkap(Wers):
    TXT_PREFIX = '  '

    HTML_ATTR = {
        "style": "padding-left: 1em"
    }
