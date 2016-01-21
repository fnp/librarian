# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#

"""
Classes for packaging ebooks for some old partners.
These should be removed from librarian to separate package,
along with custom cover images etc.

New partners shouldn't be added here, but in the partners repository.
"""

from librarian import packagers, cover
from util import makedirs


class GandalfEpub(packagers.EpubPackager):
    cover = cover.GandalfCover


class GandalfPdf(packagers.PdfPackager):
    cover = cover.GandalfCover


class BookotekaEpub(packagers.EpubPackager):
    cover = cover.BookotekaCover


class PrestigioEpub(packagers.EpubPackager):
    cover = cover.PrestigioCover
    flags = ('less-advertising',)


class PrestigioPdf(packagers.PdfPackager):
    cover = cover.PrestigioCover
    flags = ('less-advertising',)


class Virtualo(packagers.Packager):
    @staticmethod
    def utf_trunc(text, limit):
        """ truncates text to at most `limit' bytes in utf-8 """
        if text is None:
            return text
        if len(text.encode('utf-8')) > limit:
            newlimit = limit - 3
            while len(text.encode('utf-8')) > newlimit:
                text = text[:(newlimit - len(text.encode('utf-8'))) / 4]
            text += '...'
        return text

    @classmethod
    def prepare(cls, input_filenames, output_dir='', verbose=False):
        from lxml import etree
        from librarian import DirDocProvider, ParseError
        from librarian.parser import WLDocument
        from copy import deepcopy
        import os.path

        xml = etree.fromstring("""<?xml version="1.0" encoding="utf-8"?>
            <products xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"></products>""")
        product = etree.fromstring("""<product>
                <publisherProductId></publisherProductId>
                <title></title>
                <info></info>
                <description></description>
                <authors>
                    <author>
                        <names>Jan</names>
                        <lastName>Kowalski</lastName>
                    </author>
                </authors>
                <price>0.0</price>
                <language>PL</language>
            </product>""")

        try:
            for main_input in input_filenames:
                if verbose:
                    print main_input
                path, fname = os.path.realpath(main_input).rsplit('/', 1)
                provider = DirDocProvider(path)
                slug, ext = os.path.splitext(fname)

                outfile_dir = os.path.join(output_dir, slug)
                makedirs(os.path.join(output_dir, slug))

                doc = WLDocument.from_file(main_input, provider=provider)
                info = doc.book_info

                product_elem = deepcopy(product)
                product_elem[0].text = cls.utf_trunc(slug, 100)
                product_elem[1].text = cls.utf_trunc(info.title, 255)
                product_elem[2].text = cls.utf_trunc(info.description, 255)
                product_elem[3].text = cls.utf_trunc(info.source_name, 3000)
                product_elem[4][0][0].text = cls.utf_trunc(u' '.join(info.author.first_names), 100)
                product_elem[4][0][1].text = cls.utf_trunc(info.author.last_name, 100)
                xml.append(product_elem)

                cover.VirtualoCover(info).save(os.path.join(outfile_dir, slug+'.jpg'))
                outfile = os.path.join(outfile_dir, '1.epub')
                outfile_sample = os.path.join(outfile_dir, '1.sample.epub')
                doc.save_output_file(doc.as_epub(), output_path=outfile)
                doc.save_output_file(doc.as_epub(doc, sample=25), output_path=outfile_sample)
                outfile = os.path.join(outfile_dir, '1.mobi')
                outfile_sample = os.path.join(outfile_dir, '1.sample.mobi')
                doc.save_output_file(doc.as_mobi(cover=cover.VirtualoCover), output_path=outfile)
                doc.save_output_file(
                    doc.as_mobi(doc, cover=cover.VirtualoCover, sample=25),
                    output_path=outfile_sample)
        except ParseError, e:
            print '%(file)s:%(name)s:%(message)s' % {
                'file': main_input,
                'name': e.__class__.__name__,
                'message': e.message
            }

        xml_file = open(os.path.join(output_dir, 'import_products.xml'), 'w')
        xml_file.write(etree.tostring(xml, pretty_print=True, encoding=unicode).encode('utf-8'))
        xml_file.close()
