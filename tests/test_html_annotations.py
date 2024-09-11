# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import io
import unittest
from librarian.builders import HtmlBuilder
from librarian.document import WLDocument
from librarian.html import extract_annotations


class AnnotationsTests(unittest.TestCase):
    maxDiff = None

    def _test_annotation(self, expected, got, name):
        self.assertTrue(
            got[0].startswith('anchor-'),
            "%s: Unexpected anchor: '%s', should begin with 'anchor-'" % (name, got[0])
        )
        self.assertEqual(
            expected[0], got[1],
            "%s: Unexpected type, expected '%s', got '%s'" % (name, expected[0], got[1])
        )
        self.assertEqual(
            expected[1], got[2],
            "%s: Unexpected qualifier, expected '%s', got '%s'" % (name, expected[1], got[2])
        )
        self.assertEqual(
            expected[2], got[3],
            "%s: Unexpected text representation, expected '%s', got '%s'" % (name, expected[2], got[3])
        )
        exp_html = '<div class="fn-%s">%s</div>' % (expected[0], expected[3])
        self.assertEqual(
            exp_html, got[4],
            "%s: Unexpected html representation, expected '%s', got '%s'" % (name, exp_html, got[4])
        )

    def test_annotations(self):
        annotations = (
        ('<pe/>', (
            'pe',
            [],
            '[przypis edytorski]',
            '<p> [przypis edytorski]</p>'
            ),
            'Empty footnote'),

        ('<pr>Definiendum --- definiens.</pr>', (
            'pr',
            [],
            'Definiendum \u2014 definiens. [przypis redakcyjny]',
            '<p>Definiendum \u2014 definiens. [przypis redakcyjny]</p>'
            ),
            'Plain footnote.'),

        ('<pt><slowo_obce>Definiendum</slowo_obce> --- definiens.</pt>', (
            'pt',
            [],
            'Definiendum \u2014 definiens. [przypis tłumacza]',
            '<p><em class="foreign-word">Definiendum</em> \u2014 definiens. [przypis tłumacza]</p>'
            ),
            'Standard footnote.'),

        ('<pr>Definiendum (łac.) --- definiens.</pr>', (
            'pr',
            ['łac.'],
            'Definiendum (łac.) \u2014 definiens. [przypis redakcyjny]',
            '<p>Definiendum (łac.) \u2014 definiens. [przypis redakcyjny]</p>'
            ),
            'Plain footnote with qualifier'),

        ('<pe><slowo_obce>Definiendum</slowo_obce> (łac.) --- definiens.</pe>', (
            'pe',
            ['łac.'],
            'Definiendum (łac.) \u2014 definiens. [przypis edytorski]',
            '<p><em class="foreign-word">Definiendum</em> (łac.) \u2014 definiens. [przypis edytorski]</p>'
            ),
            'Standard footnote with qualifier.'),

        ('<pt> <slowo_obce>Definiendum</slowo_obce> (daw.) --- definiens.</pt>', (
            'pt',
            ['daw.'],
            'Definiendum (daw.) \u2014 definiens. [przypis tłumacza]',
            '<p> <em class="foreign-word">Definiendum</em> (daw.) \u2014 definiens. [przypis tłumacza]</p>'
            ),
            'Standard footnote with leading whitespace and qualifier.'),

        ('<pr>Definiendum (łac.) --- <slowo_obce>definiens</slowo_obce>.</pr>', (
            'pr',
            ['łac.'],
            'Definiendum (łac.) \u2014 definiens. [przypis redakcyjny]',
            '<p>Definiendum (łac.) \u2014 <em class="foreign-word">definiens</em>. [przypis redakcyjny]</p>'
            ),
            'Plain footnote with qualifier and some emphasis.'),

        ('<pe><slowo_obce>Definiendum</slowo_obce> (łac.) --- <slowo_obce>definiens</slowo_obce>.</pe>', (
            'pe',
            ['łac.'],
            'Definiendum (łac.) \u2014 definiens. [przypis edytorski]',
            '<p><em class="foreign-word">Definiendum</em> (łac.) \u2014 <em class="foreign-word">definiens</em>. [przypis edytorski]</p>'
            ),
            'Standard footnote with qualifier and some emphasis.'),

        ('<pe>Definiendum (łac.) --- definiens (some) --- more text.</pe>', (
            'pe',
            ['łac.'],
            'Definiendum (łac.) \u2014 definiens (some) \u2014 more text. [przypis edytorski]',
            '<p>Definiendum (łac.) \u2014 definiens (some) \u2014 more text. [przypis edytorski]</p>',
            ),
            'Footnote with a second parentheses and mdash.'),

        ('<pe><slowo_obce>gemajna</slowo_obce> (daw., z niem. <slowo_obce>gemein</slowo_obce>: zwykły) --- '
         'częściej: gemajn, szeregowiec w wojsku polskim cudzoziemskiego autoramentu.</pe>', (
            'pe',
            ['daw.', 'niem.'],
            'gemajna (daw., z\u00A0niem. gemein: zwykły) \u2014 częściej: gemajn, '
            'szeregowiec w\u00A0wojsku polskim cudzoziemskiego autoramentu. [przypis edytorski]',
            '<p><em class="foreign-word">gemajna</em> (daw., z\u00A0niem. <em class="foreign-word">gemein</em>: zwykły) '
            '\u2014 częściej: gemajn, szeregowiec w\u00A0wojsku polskim cudzoziemskiego autoramentu. [przypis edytorski]</p>'
            ),
            'Footnote with multiple and qualifiers and emphasis.'),
        )

        xml_src = '''<utwor><akap> %s </akap></utwor>''' % "".join(
            t[0] for t in annotations)
        html = WLDocument(
            filename=io.BytesIO(xml_src.encode('utf-8'))
        ).build(HtmlBuilder, base_url='/').get_file()
        res_annotations = list(extract_annotations(html))

        for i, (src, expected, name) in enumerate(annotations):
            with self.subTest(i=i):
                self._test_annotation(expected, res_annotations[i], name)
