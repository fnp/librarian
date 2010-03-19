# -*- coding: utf-8 -*-
import unittest
from os.path import dirname, join, realpath

from lxml import etree
from librarian import dcparser, html


def test_file_path(dir_name, file_name):
    return realpath(join(dirname(__file__), 'files', dir_name, file_name))


class TestDCParser(unittest.TestCase):
    KNOWN_RESULTS = (
        ('dcparser', 'andersen_brzydkie_kaczatko.xml', {
            'publisher': u'Fundacja Nowoczesna Polska',
            'about': u'http://wiki.wolnepodreczniki.pl/Lektury:Andersen/Brzydkie_kaczątko',
            'source_name': u'Andersen, Hans Christian (1805-1875), Baśnie, Gebethner i Wolff, wyd. 7, Kraków, 1925',
            'author': u'Andersen, Hans Christian',
            'url': u'http://wolnelektury.pl/katalog/lektura/brzydkie-kaczatko',
            'created_at': u'2007-08-14',
            'title': u'Brzydkie kaczątko',
            'kind': u'Epika',
            'source_url': u'http://www.polona.pl/dlibra/doccontent2?id=3563&dirids=4',
            'translator': u'Niewiadomska, Cecylia',
            'released_to_public_domain_at': u'1925-01-01',
            'epoch': u'Romantyzm',
            'genre': u'Baśń',
            'technical_editor': u'Gałecki, Dariusz',
            'license_description': u'Domena publiczna - tłumacz Cecylia Niewiadomska zm. 1925',
        }),
        ('dcparser', 'kochanowski_piesn7.xml', {
            'publisher': u'Fundacja Nowoczesna Polska',
            'about': u'http://wiki.wolnepodreczniki.pl/Lektury:Kochanowski/Pieśni/Pieśń_VII_(1)',
            'source_name': u'Kochanowski, Jan (1530-1584), Dzieła polskie, tom 1, oprac. Julian Krzyżanowski, wyd. 8, Państwowy Instytut Wydawniczy, Warszawa, 1976',
            'author': u'Kochanowski, Jan',
            'url': u'http://wolnelektury.pl/katalog/lektura/piesni-ksiegi-pierwsze-piesn-vii-trudna-rada-w-tej-mierze-pr',
            'created_at': u'2007-08-31',
            'title': u'Pieśń VII (Trudna rada w tej mierze: przyjdzie się rozjechać...)',
            'kind': u'Liryka',
            'source_url': u'http://www.polona.pl/Content/1499',
            'released_to_public_domain_at': u'1584-01-01',
            'epoch': u'Renesans',
            'genre': u'Pieśń',
            'technical_editor': u'Gałecki, Dariusz',
            'license_description': u'Domena publiczna - Jan Kochanowski zm. 1584 ',
        }),
        ('dcparser', 'mickiewicz_rybka.xml', {
            'publisher': u'Fundacja Nowoczesna Polska',
            'about': 'http://wiki.wolnepodreczniki.pl/Lektury:Mickiewicz/Ballady/Rybka',
            'source_name': u'Mickiewicz, Adam (1798-1855), Poezje, tom 1 (Wiersze młodzieńcze - Ballady i romanse - Wiersze do r. 1824), Krakowska Spółdzielnia Wydawnicza, wyd. 2 zwiększone, Kraków, 1922',
            'author': u'Mickiewicz, Adam',
            'url': u'http://wolnelektury.pl/katalog/lektura/ballady-i-romanse-rybka',
            'created_at': u'2007-09-06',
            'title': u'Rybka',
            'kind': u'Liryka',
            'source_url': u'http://www.polona.pl/Content/2222',
            'released_to_public_domain_at': u'1855-01-01',
            'epoch': u'Romantyzm',
            'genre': u'Ballada',
            'technical_editor': u'Sutkowska, Olga',
            'license_description': u'Domena publiczna - Adam Mickiewicz zm. 1855',
        }),
        ('dcparser', 'sofokles_antygona.xml', {
            'publisher': u'Fundacja Nowoczesna Polska',
            'about': 'http://wiki.wolnepodreczniki.pl/Lektury:Sofokles/Antygona',
            'source_name': u'Sofokles (496-406 a.C.), Antygona, Zakład Narodowy im. Ossolińskich, wyd. 7, Lwów, 1939',
            'author': u'Sofokles',
            'url': u'http://wolnelektury.pl/katalog/lektura/antygona',
            'created_at': u'2007-08-30',
            'title': u'Antygona',
            'kind': u'Dramat',
            'source_url': u'http://www.polona.pl/Content/3768',
            'translator': u'Morawski, Kazimierz',
            'released_to_public_domain_at': u'1925-01-01',
            'epoch': u'Starożytność',
            'genre': u'Tragedia',
            'technical_editor': u'Gałecki, Dariusz',
            'license_description': u'Domena publiczna - tłumacz Kazimierz Morawski zm. 1925',
        }),
        ('dcparser', 'biedrzycki_akslop.xml', {
            'publisher': u'Fundacja Nowoczesna Polska',
            'about': 'http://wiki.wolnepodreczniki.pl/Lektury:Biedrzycki/Akslop',
            'source_name': u'Miłosz Biedrzycki, * ("Gwiazdka"), Fundacja "brulion", Kraków-Warszawa, 1993',
            'author': u'Biedrzycki, Miłosz',
            'url': u'http://wolnelektury.pl/katalog/lektura/akslop',
            'created_at': u'2009-06-04',
            'title': u'Akslop',
            'kind': u'Liryka',
            'source_url': u'http://free.art.pl/mlb/gwiazdka.html#t1',
            'epoch': u'Współczesność',
            'genre': u'Wiersz',
            'technical_editor': u'Sutkowska, Olga',
            'license': u'http://creativecommons.org/licenses/by-sa/3.0/',
            'license_description': u'Creative Commons Uznanie Autorstwa - Na Tych Samych Warunkach 3.0.PL'
        }),
    )
    
    def test_parse(self):
        for dir_name, file_name, result in self.KNOWN_RESULTS:
            self.assertEqual(dcparser.parse(test_file_path(dir_name, file_name)).to_dict(), result)


class TestParserErrors(unittest.TestCase):
    def test_error(self):
        try:
            html.transform(test_file_path('erroneous', 'asnyk_miedzy_nami.xml'),
                           test_file_path('erroneous', 'asnyk_miedzy_nami.html'))
            self.fail()
        except etree.XMLSyntaxError, e:
            self.assertEqual(e.position, (25, 13))


if __name__ == '__main__':
    unittest.main()