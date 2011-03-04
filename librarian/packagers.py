# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os
from copy import deepcopy
from lxml import etree
from librarian import epub, pdf, DirDocProvider, ParseError, cover
from librarian.dcparser import BookInfo


class Packager(object):
    cover = None
    flags = None

    @classmethod
    def prepare_file(cls, main_input, output_dir, verbose=False):
        path, fname = os.path.realpath(main_input).rsplit('/', 1)
        provider = DirDocProvider(path)
        slug, ext = os.path.splitext(fname)

        if output_dir != '':
            try:
                os.makedirs(output_dir)
            except:
                pass
        outfile = os.path.join(output_dir, slug + '.' + cls.ext)
        cls.converter.transform(provider, file_path=main_input, output_file=outfile,
                cover=cls.cover, flags=cls.flags)


    @classmethod
    def prepare(cls, input_filenames, output_dir='', verbose=False):
        try:
            for main_input in input_filenames:
                if verbose:
                    print main_input
                cls.prepare_file(main_input, output_dir, verbose)
        except ParseError, e:
            print '%(file)s:%(name)s:%(message)s' % {
                'file': main_input,
                'name': e.__class__.__name__,
                'message': e.message
            }


class EpubPackager(Packager):
    converter = epub
    ext = 'epub'

class PdfPackager(Packager):
    converter = pdf
    ext = 'pdf'


class GandalfEpubPackager(EpubPackager):
    cover = cover.GandalfCover

class BookotekaEpubPackager(EpubPackager):
    cover = cover.BookotekaCover

class PrestigioEpubPackager(EpubPackager):
    cover = cover.PrestigioCover
    flags = ('less-advertising',)

class PrestigioPdfPackager(PdfPackager):
    cover = cover.PrestigioCover
    flags = ('less-advertising',)


class VirtualoEpubPackager(Packager):
    @staticmethod
    def utf_trunc(text, limit):
        """ truncates text to at most `limit' bytes in utf-8 """
        if text is None:
            return text
        orig_text = text
        if len(text.encode('utf-8')) > limit:
            newlimit = limit - 3
            while len(text.encode('utf-8')) > newlimit:
                text = text[:(newlimit - len(text.encode('utf-8'))) / 4]
            text += '...'
        return text

    @classmethod
    def prepare(cls, input_filenames, output_dir='', verbose=False):
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
                os.makedirs(os.path.join(output_dir, slug))

                info = BookInfo.from_file(main_input)

                product_elem = deepcopy(product)
                product_elem[0].text = cls.utf_trunc(slug, 100)
                product_elem[1].text = cls.utf_trunc(info.title, 255)
                product_elem[2].text = cls.utf_trunc(info.description, 255)
                product_elem[3].text = cls.utf_trunc(info.source_name, 3000)
                product_elem[4][0][0].text = cls.utf_trunc(u' '.join(info.author.first_names), 100)
                product_elem[4][0][1].text = cls.utf_trunc(info.author.last_name, 100)
                xml.append(product_elem)

                cover.VirtualoCover(
                    u' '.join(info.author.first_names + (info.author.last_name,)),
                    info.title
                    ).save(os.path.join(outfile_dir, slug+'.jpg'))
                outfile = os.path.join(outfile_dir, '1.epub')
                outfile_sample = os.path.join(outfile_dir, '1.sample.epub')
                epub.transform(provider, file_path=main_input, output_file=outfile)
                epub.transform(provider, file_path=main_input, output_file=outfile_sample, sample=25)
        except ParseError, e:
            print '%(file)s:%(name)s:%(message)s' % {
                'file': main_input,
                'name': e.__class__.__name__,
                'message': e.message
            }

        xml_file = open(os.path.join(output_dir, 'import_products.xml'), 'w')
        xml_file.write(etree.tostring(xml, pretty_print=True, encoding=unicode).encode('utf-8'))
        xml_file.close()
