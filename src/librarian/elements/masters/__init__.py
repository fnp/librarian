# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from ..base import WLElement


class Master(WLElement):
    CAN_HAVE_TEXT = False

    TXT_BOTTOM_MARGIN = 2
