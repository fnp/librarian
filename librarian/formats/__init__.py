# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#


class Format(object):
    """ Generic format class. """
    def __init__(self, doc):
        self.doc = doc

    def build(self):
        raise NotImplementedError
