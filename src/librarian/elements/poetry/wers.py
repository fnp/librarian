from ..base import WLElement


class Wers(WLElement):
    STRIP = True

    TXT_TOP_MARGIN = 1
    TXT_BOTTOM_MARGIN = 1
    TXT_LEGACY_TOP_MARGIN = 1
    TXT_LEGACY_BOTTOM_MARGIN = 0

    HTML_TAG = 'div'
    HTML_ATTRIB = {"class": "verse"}
