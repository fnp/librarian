import io
import os
from unittest import TestCase
from librarian.builders import HtmlBuilder
from librarian.document import WLDocument
from librarian.elements import WL_ELEMENTS
from .utils import get_fixture, get_all_fixtures


class HtmlExamplesTests(TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls):
        with open(get_fixture('tags', 'base.xml'), 'rb') as f:
            cls.base_xml = f.read()
    
    def test_examples(self):
        for tag in WL_ELEMENTS:
            with self.subTest(tag):
                self.tag_test(tag)
        for path in get_all_fixtures('tags'):
            if os.path.isdir(path):
                name = path.rsplit('/', 1)[1]
                self.assertIn(name, WL_ELEMENTS)

    def tag_test(self, tag):
        for fixture in get_all_fixtures(f'tags/{tag}', '*.xml'):
            with self.subTest(tag=tag, n=fixture.rsplit('/', 1)[-1].rsplit('.', 1)[0]):
                with open(fixture, 'rb') as f:
                    xml_input = f.read()
                xml_file = io.BytesIO(self.base_xml.replace(b'<!-- INPUT -->', xml_input))
                doc = WLDocument(filename=xml_file)
                html = HtmlBuilder(base_url='/').build(doc).get_bytes().decode('utf-8')

                with open(fixture.rsplit('.', 1)[0] + '.expected.html', 'r') as f:
                    expected_html = f.read()
                try:
                    with open(fixture.rsplit('.', 1)[0] + '.expected.toc.html', 'r') as f:
                        expected_toc = f.read()
                except:
                    expected_toc = ''
                try:
                    with open(fixture.rsplit('.', 1)[0] + '.expected.themes.html', 'r') as f:
                        expected_themes = f.read()
                except:
                    expected_themes = ''

                self.assertEqual(html, expected_html)
