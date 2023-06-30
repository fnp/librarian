# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from os import path
import unittest
from librarian import picture, dcparser
from tests.utils import get_all_fixtures, get_fixture


class PictureTests(unittest.TestCase):
    def test_wlpictureuri(self):
        uri = picture.WLPictureURI('http://wolnelektury.pl/katalog/obraz/angelus-novus')

    def check_load(self, xml_file):
        pi = dcparser.parse(xml_file, picture.PictureInfo)
        self.assertIsNotNone(pi)
        self.assertIsInstance(pi, picture.PictureInfo)
    
    def test_load(self):
        for fixture in get_all_fixtures('picture', '*.xml'):
            with self.subTest(fixture=fixture):
                self.check_load(fixture)

    def test_wlpicture(self):
        with open(get_fixture('picture', 'angelus-novus.xml')) as f:
            wlp = picture.WLPicture.from_file(f)
        pi = wlp.picture_info

        self.assertEqual(pi.type[0], "Image")
        self.assertEqual(pi.mime_type, 'image/jpeg')
        self.assertEqual(wlp.mime_type, 'image/jpeg')
        self.assertEqual(wlp.slug, 'angelus-novus')
        self.assertTrue(path.exists(wlp.image_path))
    
        f = wlp.image_file()
        f.close()


    def test_picture_parts(self):
        with open(get_fixture('picture', 'angelus-novus.xml')) as f:
            wlp = picture.WLPicture.from_file(f)
        parts = list(wlp.partiter())
        expect_parts = 4
        self.assertEqual(len(parts), expect_parts, "there should be %d parts of the picture" % expect_parts)
        motifs = set()
        names = set()

        for p in parts:
            for m in p['themes']:
                motifs.add(m)
        for p in parts:
            if p['object']:
                names.add(p['object'])

        self.assertEqual(motifs, {'anioł historii', 'spojrzenie'}, "missing motifs, got: %s" % motifs)
        self.assertEqual(names, {'obraz cały', 'skrzydło'}, 'missing objects, got: %s' % names)
