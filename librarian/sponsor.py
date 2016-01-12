# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from librarian import get_resource


def sponsor_logo(name):
    return {
        'Narodowe Centrum Kultury': get_resource('res/sponsors/nck.png')
    }.get(name.strip())
