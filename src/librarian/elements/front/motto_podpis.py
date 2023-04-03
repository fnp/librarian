from ..base import WLElement


class MottoPodpis(WLElement):
    SHOULD_HAVE_ID = True
    HTML_TAG = "p"
    EPUB_CLASS = HTML_CLASS = "motto_podpis"

    EPUB_TAG = "div"
    
