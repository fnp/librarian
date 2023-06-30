# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..paragraphs import Akap


class MiejsceCzas(Akap):
    SHOULD_HAVE_ID = True

    EPUB_TAG = "div"
    EPUB_CLASS = HTML_CLASS = 'place-and-time'
    
