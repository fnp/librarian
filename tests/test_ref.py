# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from unittest import TestCase
from librarian.builders import builders
from librarian.document import WLDocument
from tests.utils import get_fixture
from lxml import etree


class RefTests(TestCase):
    def test_snippet(self):
        doc = WLDocument(filename=get_fixture('text', 'miedzy-nami-nic-nie-bylo.xml'))

        hb = builders['html']()
        hb.assign_ids(doc.tree)

        refs = []
        for ref in doc.references():
            snippet = ref.get_snippet()
            b = builders['html-snippet']()

            for s in snippet:
                s.html_build(b)
            refs.append(
                '\n'.join((
                    ref.get_link(),
                    b.output().get_bytes().decode('utf-8')
                ))
            )
        output = '\n\n'.join(refs)
        with open(get_fixture('text', 'asnyk_miedzy_nami_refs.html')) as f:
            self.assertEqual(output, f.read())
    
