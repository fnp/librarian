# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Animacja(WLElement):
    SHOULD_HAVE_ID = True

    HTML_TAG = 'div'
    HTML_CLASS = "animacja cycle-slideshow"
    HTML_ATTR = {
        "data-cycle-pause-on-hover": "true",
        "data-cycle-next": "> img",
        "data-cycle-fx": "fadeout",
        "data-cycle-paused": "true",
    }
