from ..base import WLElement


class DidaskTekst(WLElement):
    TXT_PREFIX = "/ "
    TXT_SUFFIX = " /"

    HTML_TAG = "em"
    HTML_CLASS = "didaskalia"
