from ..paragraphs import Akap


class MiejsceCzas(Akap):
    SHOULD_HAVE_ID = True

    EPUB_TAG = "div"
    EPUB_CLASS = HTML_CLASS = 'place-and-time'
    
