from datetime import date
import os
import tempfile
from ebooklib import epub
from lxml import etree
import six
from librarian import functions, OutputFile, get_resource, XHTMLNS
from librarian.cover import make_cover
from librarian.embeds.mathml import MathML
import librarian.epub
from librarian.fonts import strip_font
from librarian.fundraising import FUNDRAISING




class Xhtml:
    def __init__(self):
        self.element = etree.XML('''<html xmlns="http://www.w3.org/1999/xhtml"><head><link rel="stylesheet" href="style.css" type="text/css"/><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><title>WolneLektury.pl</title></head><body/></html>''')

    @property
    def title(self):
        return self.element.find('.//' + XHTMLNS('title'))
        
    @property
    def body(self):
        return self.element.find('.//' + XHTMLNS('body'))


class Builder:
    file_extension = None

    def __init__(self, base_url=None):
        self._base_url = base_url or 'file:///home/rczajka/for/fnp/librarian/temp~/maly/img/'
        self.footnotes = etree.Element('div', id='footnotes')

        self.cursors = {
#            None: None,
#            'header': self.header,
            'footnotes': self.footnotes,
        }
        self.current_cursors = []

        self.toc_base = 0

    @property
    def cursor(self):
        return self.current_cursors[-1]

    def enter_fragment(self, fragment):
        self.current_cursors.append(self.cursors[fragment])

    def exit_fragment(self):
        self.current_cursors.pop()

    def create_fragment(self, name, element):
        assert name not in self.cursors
        self.cursors[name] = element

    def forget_fragment(self, name):
        del self.cursors[name]



    @property
    def base_url(self):
        if self._base_url is not None:
            return self._base_url
        else:
            return 'https://wolnelektury.pl/media/book/pictures/{}/'.format(self.document.meta.url.slug)


    # Base URL should be on Document level, not builder.
    def build(self, document, **kwargs):
        """Should return an OutputFile with the output."""
        raise NotImplementedError()


class EpubBuilder(Builder):
    file_extension = 'epub'

    def __init__(self, *args, **kwargs):
        self.chars = set()
        self.fundr = 0
        super().__init__(*args, **kwargs)
    
    def build(self, document, **kwargs):
        # replace_characters -- nie, robimy to na poziomie elementów
        
        # hyphenator (\00ad w odp. miejscach) -- jeśli już, to też powinno to się dziać na poziomie elementów
        # spójniki (\u00a0 po)-- jeśli już, to na poziomie elementów
        # trick na dywizy: &#xad;&#8288;-

        # do toc trafia:
        #   początek z KAŻDEGO PLIKU xml
        
        # zliczamy zbiór użytych znaków

        # flagi:
        # mieliśmy taką flagę less-advertising, używaną tylko dla Prestigio; już nie używamy.

        # @editors = document.editors() (jako str)
        # @funders = join(meta.funders)
        # @thanks = meta.thanks


        self.output = output = epub.EpubBook()
        self.document = document

        self.set_metadata()
        

        self.add_cover()
        
        self.add_title_page()
        self.add_toc()



        self.start_chunk()

        self.add_toc_entry(
            None,
            'Początek utworu', # i18n
            0
        )
        self.output.guide.append({
            "type": "text",
            "title": "Początek",
            "href": "part1.xhtml"
        })


        self.build_document(self.document)

        
        self.close_chunk()

        self.add_annotations()
        self.add_support_page()
        self.add_last_page()


        e = len(self.output.spine) - 3 - 3
        nfunds = len(FUNDRAISING)
        if e > 16:
            nfunds *= 2

        # COUNTING CHARACTERS?
        for f in range(nfunds):
            spine_index = int(4 + (f / nfunds * e) + f)

            h = Xhtml()
            h.body.append(
                etree.XML('<div id="book-text"><div class="fundraising">' + FUNDRAISING[f % len(FUNDRAISING)] + '</div></div>')
            )
            self.add_html(h.element, file_name='fund%d.xhtml' % f, spine=spine_index)

        self.add_fonts()

        output_file = tempfile.NamedTemporaryFile(
            prefix='librarian', suffix='.epub',
            delete=False)
        output_file.close()
        epub.write_epub(output_file.name, output, {'epub3_landmark': False})
        return OutputFile.from_filename(output_file.name)

    def build_document(self, document):
        self.toc_precedences = []

        self.start_chunk()


        document.tree.getroot().epub_build(self)
        if document.meta.parts:
            self.start_chunk()

            self.start_element('div', {'class': 'title-page'})
            self.start_element('h1', {'class': 'title'})
            self.push_text(document.meta.title)
            self.end_element()
            self.end_element()

            ######
            # 160
            # translators
            # working copy?
            # ta lektura
            # tanks
            # utwor opracowany
            # isbn
            # logo

            for child in document.children:
                self.start_chunk()
                self.add_toc_entry(None, child.meta.title, 0)
                self.build_document(child)

        self.shift_toc_base()
            
    
    def add_title_page(self):
        html = Xhtml()
        html.title.text = "Strona tytułowa"
        bt = etree.SubElement(html.body, 'div', **{'class': 'book-text'})
        tp = etree.SubElement(bt, 'div', **{'class': 'title-page'})

        # Tak jak jest teraz – czy może być jednocześnie
        # no „autor_utworu”
        # i „dzieło nadrzędne”
        # wcześniej mogło być dzieło nadrzędne,

        e = self.document.tree.find('//autor_utworu')
        if e is not None:
            etree.SubElement(tp, 'h2', **{'class': 'author'}).text = e.raw_printable_text()
        e = self.document.tree.find('//nazwa_utworu')
        if e is not None:
            etree.SubElement(tp, 'h1', **{'class': 'title'}).text = e.raw_printable_text()

        if not len(tp):
            for author in self.document.meta.authors:
                etree.SubElement(tp, 'h2', **{'class': 'author'}).text = author.readable()
            etree.SubElement(tp, 'h1', **{'class': 'title'}).text = self.document.meta.title

#                <xsl:apply-templates select="//nazwa_utworu | //podtytul | //dzielo_nadrzedne" mode="poczatek"/>
#        else:
#                            <xsl:apply-templates select="//dc:creator" mode="poczatek"/>
#                <xsl:apply-templates select="//dc:title | //podtytul | //dzielo_nadrzedne" mode="poczatek"/>

        etree.SubElement(tp, 'p', **{"class": "info"}).text = '\u00a0'

        if self.document.meta.translators:
            p = etree.SubElement(tp, 'p', **{'class': 'info'})
            p.text = 'tłum. ' + ', '.join(t.readable() for t in self.document.meta.translators)
                
        #<p class="info">[Kopia robocza]</p>

        p = etree.XML("""<p class="info">
              <a>Ta lektura</a>, podobnie jak tysiące innych, jest dostępna on-line na stronie
              <a href="http://www.wolnelektury.pl/">wolnelektury.pl</a>.
            </p>""")
        p[0].attrib['href'] = str(self.document.meta.url)
        tp.append(p)

        if self.document.meta.thanks:
            etree.SubElement(tp, 'p', **{'class': 'info'}).text = self.document.meta.thanks
        
        tp.append(etree.XML("""
          <p class="info">
            Utwór opracowany został w&#160;ramach projektu<a href="http://www.wolnelektury.pl/"> Wolne Lektury</a> przez<a href="http://www.nowoczesnapolska.org.pl/"> fundację Nowoczesna Polska</a>.
          </p>
        """))

        if self.document.meta.isbn_epub:
            etree.SubElement(tp, 'p', **{"class": "info"}).text = self.document.meta.isbn_epub

        tp.append(etree.XML("""<p class="footer info">
            <a href="http://www.wolnelektury.pl/"><img src="logo_wolnelektury.png" alt="WolneLektury.pl" /></a>
        </p>"""))

        self.add_html(
            html.element,
            file_name='title.xhtml',
            spine=True,
            toc='Strona tytułowa' # TODO: i18n
        )

        self.add_file(
            get_resource('res/wl-logo-small.png'),
            file_name='logo_wolnelektury.png',
            media_type='image/png'
        )
    
    def set_metadata(self):
        self.output.set_identifier(
            str(self.document.meta.url))
        self.output.set_language(
            functions.lang_code_3to2(self.document.meta.language)
        )
        self.output.set_title(self.document.meta.title)

        for i, author in enumerate(self.document.meta.authors):
            self.output.add_author(
                author.readable(),
                file_as=six.text_type(author),
                uid='creator{}'.format(i)
            )
        for translator in self.document.meta.translators:
            self.output.add_author(
                translator.readable(),
                file_as=six.text_type(translator),
                role='trl',
                uid='translator{}'.format(i)
            )
        for publisher in self.document.meta.publisher:
            self.output.add_metadata("DC", "publisher", publisher)

        self.output.add_metadata("DC", "date", self.document.meta.created_at)

        


    def add_toc(self):
        item = epub.EpubNav()
        self.output.add_item(item)
        self.output.spine.append(item)
        self.output.add_item(epub.EpubNcx())

        self.output.toc.append(
            epub.Link(
                "nav.xhtml",
                "Spis treści",
                "nav"
            )
        )

    

    def add_support_page(self):
        self.add_file(
            get_resource('epub/support.xhtml'),
            spine=True,
            toc='Wesprzyj Wolne Lektury'
        )

        self.add_file(
            get_resource('res/jedenprocent.png'),
            media_type='image/png'
        )
        self.add_file(
            get_resource('epub/style.css'),
            media_type='text/css'
        )


    def add_file(self, path=None, content=None,
                 media_type='application/xhtml+xml',
                 file_name=None, uid=None,
                 spine=False, toc=None):

        # update chars?
        # jakieś tam ścieśnianie białych znaków?

        if content is None:
            with open(path, 'rb') as f:
                content = f.read()
            if file_name is None:
                file_name = path.rsplit('/', 1)[-1]

        if uid is None:
            uid = file_name.split('.', 1)[0]

        item = epub.EpubItem(
            uid=uid,
            file_name=file_name,
            media_type=media_type,
            content=content
        )

        self.output.add_item(item)
        if spine:
            if spine is True:
                self.output.spine.append(item)
            else:
                self.output.spine.insert(spine, item)

        if toc:
            self.output.toc.append(
                epub.Link(
                    file_name,
                    toc,
                    uid
                )
            )

    def add_html(self, html_tree, **kwargs):
        html = etree.tostring(
            html_tree, pretty_print=True, xml_declaration=True,
            encoding="utf-8",
            doctype='<!DOCTYPE html>'
        )

        html = librarian.epub.squeeze_whitespace(html)

        self.add_file(
            content=html,
            **kwargs
        )
            
        
    def add_fonts(self):
        print("".join(sorted(self.chars)))
        # TODO: optimizer
        for fname in ('DejaVuSerif.ttf', 'DejaVuSerif-Bold.ttf',
                      'DejaVuSerif-Italic.ttf', 'DejaVuSerif-BoldItalic.ttf'):
            self.add_file(
                content=strip_font(
                    get_resource('fonts/' + fname),
                    self.chars
                ),
                file_name=fname,
                media_type='font/ttf'
            )

    def start_chunk(self):
        if getattr(self, 'current_chunk', None) is not None:
            if not len(self.current_chunk):
                return
            self.close_chunk()
        self.current_chunk = etree.Element(
            'div',
            id="book-text"
        )
        self.cursors[None] = self.current_chunk
        self.current_cursors.append(self.current_chunk)

        self.section_number = 0
        

    def close_chunk(self):
        assert self.cursor is self.current_chunk
        ###### -- what if we're inside?

        chunk_no = getattr(
            self,
            'chunk_counter',
            1
        )
        self.chunk_counter = chunk_no + 1

        html = Xhtml()
        html.body.append(self.current_chunk)
        
        self.add_html(
            ## html container from template.
            #self.current_chunk,
            html.element,
            file_name='part%d.xhtml' % chunk_no,
            spine=True,
            
        )
        self.current_chunk = None
        self.current_cursors.pop()

    def start_element(self, tag, attr):
        self.current_cursors.append(
            etree.SubElement(self.cursor, tag, **attr)
        )
        
    def end_element(self):
        self.current_cursors.pop()
        
    def push_text(self, text):
        self.chars.update(text)
        if len(self.cursor):
            self.cursor[-1].tail = (self.cursor[-1].tail or '') + text
        else:
            self.cursor.text = (self.cursor.text or '') + text


    def assign_image_number(self):
        image_number = getattr(self, 'image_number', 0)
        self.image_number = image_number + 1
        return image_number

    def assign_footnote_number(self):
        number = getattr(self, 'footnote_number', 1)
        self.footnote_number = number + 1
        return number

    def assign_section_number(self):
        number = getattr(self, 'section_number', 1)
        self.section_number = number + 1
        return number

    def assign_mathml_number(self):
        number = getattr(self, 'mathml_number', 0)
        self.mathml_number = number + 1
        return number

    
    def add_toc_entry(self, fragment, name, precedence):
        if precedence:
            while self.toc_precedences and self.toc_precedences[-1] >= precedence:
                self.toc_precedences.pop()
        else:
            self.toc_precedences = []

        real_level = self.toc_base + len(self.toc_precedences)
        if precedence:
            self.toc_precedences.append(precedence)
        else:
            self.toc_base += 1
        
        part_number = getattr(
            self,
            'chunk_counter',
            1
        )
        filename = 'part%d.xhtml' % part_number
        uid = filename.split('.')[0]
        if fragment:
            filename += '#' + fragment
            uid += '-' + fragment

        toc = self.output.toc
        for l in range(1, real_level):
            if isinstance(toc[-1], epub.Link):
                toc[-1] = [toc[-1], []]
            toc = toc[-1][1]

        toc.append(
            epub.Link(
                filename,
                name,
                uid
            )
        )

    def shift_toc_base(self):
        self.toc_base -= 1
        

    def add_last_page(self):
        html = Xhtml()
        m = self.document.meta
        
        html.title.text = 'Strona redakcyjna'
        d = etree.SubElement(html.body, 'div', id='book-text')

        newp = lambda: etree.SubElement(d, 'p', {'class': 'info'})

        p = newp()
        if m.license:
            p.text = """
                      Ten utwór jest udostępniony na licencji
                      """
            etree.SubElement(p, 'a', href=m.license).text = m.license_description
        else:
            p.text = """
                    Ten utwór nie jest objęty majątkowym prawem autorskim i znajduje się w domenie
                    publicznej, co oznacza że możesz go swobodnie wykorzystywać, publikować
                    i rozpowszechniać. Jeśli utwór opatrzony jest dodatkowymi materiałami
                    (przypisy, motywy literackie etc.), które podlegają prawu autorskiemu, to
                    te dodatkowe materiały udostępnione są na licencji
                    """
            a = etree.SubElement(p, "a", href="http://creativecommons.org/licenses/by-sa/3.0/")
            a.text = """Creative Commons
                    Uznanie Autorstwa – Na Tych Samych Warunkach 3.0 PL"""
            a.tail = "."


        p = newp()
        p.text = 'Źródło: '
        etree.SubElement(
            p, 'a', href=str(m.url),
            title=', '.join((
                ', '.join(p.readable() for p in m.authors),
                m.title
            ))
        ).text = str(m.url)

        newp().text = 'Tekst opracowany na podstawie: ' + m.source_name

        newp().text = """
              Wydawca:
              """ + ", ".join(p for p in m.publisher)

        if m.description:
            newp().text = m.description


        if m.editors:
            newp().text = 'Opracowanie redakcyjne i przypisy: %s.' % (
                ', '.join(e.readable() for e in sorted(self.document.editors())))

        if m.funders:
            etree.SubElement(d, 'p', {'class': 'minor-info'}).text = '''Publikację wsparli i wsparły:
            %s.''' % (', '.join(m.funders))

        if m.cover_by:
            p = newp()
            p.text = 'Okładka na podstawie: '
            if m.cover_source:
                etree.SubElement(
                    p,
                    'a',
                    href=m.cover_source
                ).text = m.cover_by
            else:
                p.text += m.cover_by
            
        if m.isbn_epub:
            newp().text = m.isbn_epub

        newp().text = '\u00a0'

        p = newp()
        p.attrib['class'] = 'minor-info'
        p.text = '''
              Plik wygenerowany dnia '''
        span = etree.SubElement(p, 'span', id='file_date')
        span.text = str(date.today())
        span.tail = '''.
          '''
        
        self.add_html(
            html.element,
            file_name='last.xhtml',
            toc='Strona redakcyjna',
            spine=True
        )


    def add_annotations(self):
        if not len(self.footnotes):
            return

        html = Xhtml()
        html.title.text = 'Przypisy'
        d = etree.SubElement(
            etree.SubElement(
                html.body,
                'div',
                id='book-text'
            ),
            'div',
            id='footnotes'
        )
        
        etree.SubElement(
            d,
            'h2',
        ).text = 'Przypisy:'

        d.extend(self.footnotes)
        
        self.add_html(
            html.element,
            file_name='annotations.xhtml',
            spine=True,
            toc='Przypisy'
        )

    def add_cover(self):
        # TODO: allow other covers

        cover_maker = make_cover

        cover_file = six.BytesIO()
        cover = cover_maker(self.document.meta)
        cover.save(cover_file)
        cover_name = 'cover.%s' % cover.ext()

        self.output.set_cover(
            file_name=cover_name,
            content=cover_file.getvalue(),
            create_page = False
        )
        ci = ('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en" xml:lang="en">
 <head>
  <title>Okładka</title>
  <style>
    body { margin: 0em; padding: 0em; }
    img { width: 100%%; }
  </style>
 </head>
 <body>
   <img src="cover.%s" alt="Okładka" />
 </body>
</html>''' % cover.ext()).encode('utf-8')
        self.add_file(file_name='cover.xhtml', content=ci)

        self.output.spine.append('cover')
        self.output.guide.append({
            'type': 'cover',
            'href': 'cover.xhtml',
            'title': 'Okładka'
        })

    def mathml(self, element):
        name = "math%d.png" % self.assign_mathml_number()
        self.add_file(
            content=MathML(element).to_latex().to_png().data,
            media_type='image/png',
            file_name=name
        )
        return name
