# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from __future__ import unicode_literals

import unittest
from librarian.html import extract_fragments
from .utils import get_fixture


class FragmentsTest(unittest.TestCase):
    maxDiff = None

    def test_fragments(self):
        expected_output_file_path = get_fixture('text', 'asnyk_miedzy_nami_fragments.html')

        closed_fragments, open_fragments = extract_fragments(
            get_fixture('text', 'asnyk_miedzy_nami_expected.html'))
        assert not open_fragments
        fragments_text = u"\n\n".join(u"%s: %s\n%s" % (f.id, f.themes, f) for f in sorted(closed_fragments.values(), key=lambda f: f.id))
        self.assertEqual(fragments_text, open(expected_output_file_path, 'rb').read().decode('utf-8'))
