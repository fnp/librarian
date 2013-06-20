# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from lxml import etree
from librarian import IOFile, RDFNS, DCNS, Format
from xmlutils import Xmill, tag, tagged, ifoption, tag_open_close
from librarian import functions
import re
import random
from copy import deepcopy

IMAGE_THUMB_WIDTH = 300

try:
    from fnpdjango.utils.text.slughifi import slughifi
    def naglowek_to_anchor(naglowek):
        return slughifi(naglowek.text)
except ImportError:
    from urllib import quote
    def naglowek_to_anchor(naglowek):
        return quote(re.sub(r" +", " ", naglowek.text.strip()))
    
    

class EduModule(Xmill):
    def __init__(self, options=None):
        super(EduModule, self).__init__(options)
        self.activity_counter = 0
        self.exercise_counter = 0

        # text filters
        def swap_endlines(txt):
            if self.options['strofa']:
                txt = txt.replace("/\n", "<br/>\n")
            return txt
        self.register_text_filter(functions.substitute_entities)
        self.register_escaped_text_filter(swap_endlines)

    @tagged('div', 'stanza')
    def handle_strofa(self, element):
        self.options = {'strofa': True}
        return "", ""

    def handle_powiesc(self, element):
        return u"""
<div class="module" id="book-text">
<!-- <span class="teacher-toggle">
  <input type="checkbox" name="teacher-toggle" id="teacher-toggle"/>
  <label for="teacher-toggle">Pokaż treść dla nauczyciela</label>
 </span>-->

""", u"</div>"

    handle_autor_utworu = tag("span", "author")
    handle_dzielo_nadrzedne = tag("span", "collection")
    handle_podtytul = tag("span", "subtitle")
    handle_naglowek_akt = handle_naglowek_czesc = handle_srodtytul = tag("h2")
    handle_naglowek_scena = tag('h2')
    handle_naglowek_osoba = handle_naglowek_podrozdzial = tag('h3')
    handle_akap = handle_akap_dialog = handle_akap_cd = tag('p', 'paragraph')

    handle_wyroznienie = tag('em')
    handle_tytul_dziela = tag('em', 'title')
    handle_slowo_obce = tag('em', 'foreign')

    def handle_nazwa_utworu(self, element):
        toc = []
        for naglowek in element.getparent().findall('.//naglowek_rozdzial'):
            a = etree.Element("a")
            a.attrib["href"] = "#" + naglowek_to_anchor(naglowek)
            a.text = naglowek.text
            atxt = etree.tostring(a, encoding=unicode)
            toc.append("<li>%s</li>" % atxt)
        toc = "<ul class='toc'>%s</ul>" % "".join(toc)
        add_header = "Lekcja: " if self.options['wldoc'].book_info.type in ('course', 'synthetic') else ''
        return "<h1 class='title' id='top'>%s" % add_header, "</h1>" + toc

    def handle_naglowek_rozdzial(self, element):
        return_to_top = u"<a href='#top' class='top-link'>wróć do spisu treści</a>"
        pre, post = tag_open_close("h2", id=naglowek_to_anchor(element))
        return return_to_top + pre, post

    def handle_uwaga(self, _e):
        return None

    def handle_aktywnosc(self, element):
        self.activity_counter += 1
        self.options = {
            'activity': True,
            'activity_counter': self.activity_counter,
            }
        submill = EduModule(dict(self.options.items() + {'sub_gen': True}.items()))

        if element.xpath('opis'):
            opis = submill.generate(element.xpath('opis')[0])
        else:
            opis = ''

        n = element.xpath('wskazowki')
        if n: wskazowki = submill.generate(n[0])

        else: wskazowki = ''
        n = element.xpath('pomoce')

        if n: pomoce = submill.generate(n[0])
        else: pomoce = ''

        forma = ''.join(element.xpath('forma/text()'))

        czas = ''.join(element.xpath('czas/text()'))

        counter = self.activity_counter

        return u"""
<div class="activity">
 <div class="text">
  <span class="act_counter">%(counter)d.</span>
  %(opis)s""" % locals(), \
u"""%(wskazowki)s
 </div>
 <aside class="info">
  <section class="infobox time"><h1>Czas</h1><p>%(czas)s min</p></section>
  <section class="infobox kind"><h1>Metoda</h1><p>%(forma)s</p></section>
  %(pomoce)s
 </aside>
 <div class="clearboth"></div>
</div>
""" % locals()

    handle_opis = ifoption(sub_gen=True)(tag('div', 'description'))
    handle_wskazowki = ifoption(sub_gen=True)(tag('div', ('hints', 'teacher')))

    @ifoption(sub_gen=True)
    @tagged('section', 'infobox materials')
    def handle_pomoce(self, _):
        return """<h1>Pomoce</h1>""", ""

    def handle_czas(self, *_):
        return

    def handle_forma(self, *_):
        return

    def handle_cwiczenie(self, element):
        exercise_handlers = {
            'wybor': Wybor,
            'uporzadkuj': Uporzadkuj,
            'luki': Luki,
            'zastap': Zastap,
            'przyporzadkuj': Przyporzadkuj,
            'prawdafalsz': PrawdaFalsz
            }

        typ = element.attrib['typ']
        self.exercise_counter += 1
        self.options = {'exercise_counter': self.exercise_counter}
        handler = exercise_handlers[typ](self.options)
        return handler.generate(element)

    # Lists
    def handle_lista(self, element, attrs={}):
        ltype = element.attrib.get('typ', 'punkt')
        if not element.findall("punkt"):
            if ltype == 'czytelnia':
                return '<p>W przygotowaniu.</p>'
            else:
                return None
        if ltype == 'slowniczek':
            surl = element.attrib.get('src', None)
            if surl is None:
                # print '** missing src on <slowniczek>, setting default'
                surl = 'http://edukacjamedialna.edu.pl/lekcje/slowniczek/'
            sxml = None
            if surl:
                sxml = etree.fromstring(self.options['provider'].by_uri(surl).get_string())
            self.options = {'slowniczek': True, 'slowniczek_xml': sxml }
            pre, post = '<div class="slowniczek">', '</div>'
            if self.options['wldoc'].book_info.url.slug != 'slowniczek':
                post += u'<p class="see-more"><a href="%s">Zobacz cały słowniczek.</a></p>' % surl
            return pre, post

        listtag = {'num': 'ol',
               'punkt': 'ul',
               'alfa': 'ul',
               'czytelnia': 'ul'}[ltype]

        classes = attrs.get('class', '')
        if classes: del attrs['class']

        attrs_s = ' '.join(['%s="%s"' % kv for kv in attrs.items()])
        if attrs_s: attrs_s = ' ' + attrs_s

        return '<%s class="lista %s %s"%s>' % (listtag, ltype, classes, attrs_s), '</%s>' % listtag

    def handle_punkt(self, element):
        if self.options['slowniczek']:
            return '<dl>', '</dl>'
        else:
            return '<li>', '</li>'

    def handle_definiendum(self, element):
        nxt = element.getnext()
        definiens_s = ''

        if not element.text:
            print "!! Empty <definiendum/>"
            return None

        # let's pull definiens from another document
        if self.options['slowniczek_xml'] is not None and (nxt is None or nxt.tag != 'definiens'):
            sxml = self.options['slowniczek_xml']
            defloc = sxml.xpath("//definiendum[text()='%s']" % element.text)
            if defloc:
                definiens = defloc[0].getnext()
                if definiens.tag == 'definiens':
                    subgen = EduModule(self.options)
                    definiens_s = subgen.generate(definiens)
            else:
                print '!! Missing definiendum in source:', element.text

        return u"<dt>", u"</dt>" + definiens_s

    def handle_definiens(self, element):
        return u"<dd>", u"</dd>"

    def handle_podpis(self, element):
        return u"""<div class="caption">""", u"</div>"

    def handle_tabela(self, element):
        has_frames = int(element.attrib.get("ramki", "0"))
        if has_frames: frames_c = "framed"
        else: frames_c = ""
        return u"""<table class="%s">""" % frames_c, u"</table>"

    def handle_wiersz(self, element):
        return u"<tr>", u"</tr>"

    def handle_kol(self, element):
        return u"<td>", u"</td>"

    def handle_rdf__RDF(self, _):
        # ustal w opcjach  rzeczy :D
        return

    def handle_link(self, element):
        if 'url' in element.attrib:
            return tag('a', href=element.attrib['url'])(self, element)
        elif 'material' in element.attrib:
            material_err = u' [BRAKUJĄCY MATERIAŁ]'
            slug = element.attrib['material']
            make_url = lambda f: self.options['urlmapper'] \
              .url_for_material(slug, f)

            if 'format' in element.attrib:
                formats = re.split(r"[, ]+",
                               element.attrib['format'])
            else:
                formats = [None]

            formats = self.options['urlmapper'].materials(slug)

            try:
                def_href = make_url(formats[0][0])
                def_err = u""
            except (IndexError, self.options['urlmapper'].MaterialNotFound):
                def_err = material_err
                def_href = u""
            fmt_links = []
            for f in formats[1:]:
                try:
                    fmt_links.append(u'<a href="%s">%s</a>' % (make_url(f[0]), f[0].upper()))
                except self.options['urlmapper'].MaterialNotFound:
                    fmt_links.append(u'<a>%s%s</a>' % (f[0].upper(), material_err))
            more_links = u' (%s)' % u', '.join(fmt_links) if fmt_links else u''

            return u"<a href='%s'>" % def_href, u'%s</a>%s' % (def_err, more_links)

    def handle_obraz(self, element):
        name = element.attrib.get('nazwa', '').strip()
        if not name:
            print '!! <obraz> missing "nazwa"'
            return
        alt = element.attrib.get('alt', '')
        if not alt:
            print '** <obraz> missing "alt"'
        slug, ext = name.rsplit('.', 1)
        url = self.options['urlmapper'].url_for_image(slug, ext)
        thumb_url = self.options['urlmapper'].url_for_image(slug, ext, IMAGE_THUMB_WIDTH)
        e = etree.Element("a", attrib={"href": url, "class": "image"})
        e.append(etree.Element("img", attrib={"src": thumb_url, "alt": alt,
                    "width": str(IMAGE_THUMB_WIDTH)}))
        return etree.tostring(e, encoding=unicode), u""

    def handle_video(self, element):
        url = element.attrib.get('url')
        if not url:
            print '!! <video> missing url'
            return
        m = re.match(r'(?:https?://)?(?:www.)?youtube.com/watch\?(?:.*&)?v=([^&]+)(?:$|&)', url)
        if not m:
            print '!! unknown <video> url scheme:', url
            return
        return """<iframe width="630" height="384" src="http://www.youtube.com/embed/%s"
            frameborder="0" allowfullscreen></iframe>""" % m.group(1), ""


class Exercise(EduModule):
    INSTRUCTION = ""
    def __init__(self, *args, **kw):
        self.question_counter = 0
        super(Exercise, self).__init__(*args, **kw)
        self.instruction_printed = False

    @tagged('div', 'description')
    def handle_opis(self, element):
        return "", self.get_instruction()

    def handle_rozw_kom(self, element):
        return u"""<div style="display:none" class="comment">""", u"""</div>"""

    def handle_cwiczenie(self, element):
        self.options = {'exercise': element.attrib['typ']}
        self.question_counter = 0
        self.piece_counter = 0

        pre = u"""
<div class="exercise %(typ)s" data-type="%(typ)s">
<form action="#" method="POST">
<h3>Zadanie %(exercies_counter)d</h3>
<div class="buttons">
<span class="message"></span>
<input type="button" class="check" value="sprawdź"/>
<input type="button" class="retry" style="display:none" value="spróbuj ponownie"/>
<input type="button" class="solutions" value="pokaż rozwiązanie"/>
<input type="button" class="reset" value="reset"/>
</div>

""" % {'exercies_counter': self.options['exercise_counter'], 'typ': element.attrib['typ']}
        post = u"""
<div class="buttons">
<span class="message"></span>
<input type="button" class="check" value="sprawdź"/>
<input type="button" class="retry" style="display:none" value="spróbuj ponownie"/>
<input type="button" class="solutions" value="pokaż rozwiązanie"/>
<input type="button" class="reset" value="reset"/>
</div>
</form>
</div>
"""
        # Add a single <pytanie> tag if it's not there
        if not element.xpath(".//pytanie"):
            qpre, qpost = self.handle_pytanie(element)
            pre = pre + qpre
            post = qpost + post
        return pre, post

    def handle_pytanie(self, element):
        """This will handle <cwiczenie> element, when there is no <pytanie>
        """
        add_class = ""
        self.question_counter += 1
        self.piece_counter = 0
        solution = element.attrib.get('rozw', None)
        if solution: solution_s = ' data-solution="%s"' % solution
        else: solution_s = ''

        handles = element.attrib.get('uchwyty', None)
        if handles:
            add_class += ' handles handles-%s' % handles
            self.options = {'handles': handles}

        minimum = element.attrib.get('min', None)
        if minimum: minimum_s = ' data-minimum="%d"' % int(minimum)
        else: minimum_s = ''

        return '<div class="question%s" data-no="%d" %s>' %\
            (add_class, self.question_counter, solution_s + minimum_s), \
            "</div>"

    def get_instruction(self):
        if not self.instruction_printed:
            self.instruction_printed = True
            if self.INSTRUCTION:
                return u'<span class="instruction">%s</span>' % self.INSTRUCTION
            else:
                return ""
        else:
            return ""



class Wybor(Exercise):
    def handle_cwiczenie(self, element):
        pre, post = super(Wybor, self).handle_cwiczenie(element)
        is_single_choice = True
        pytania = element.xpath(".//pytanie")
        if not pytania:
            pytania = [element]
        for p in pytania:
            solutions = re.split(r"[, ]+", p.attrib.get('rozw', ''))
            if len(solutions) != 1:
                is_single_choice = False
                break
            choices = p.xpath(".//*[@nazwa]")
            uniq = set()
            for n in choices: uniq.add(n.attrib.get('nazwa', ''))
            if len(choices) != len(uniq):
                is_single_choice = False
                break

        self.options = {'single': is_single_choice}
        return pre, post

    def handle_punkt(self, element):
        if self.options['exercise'] and element.attrib.get('nazwa', None):
            qc = self.question_counter
            self.piece_counter += 1
            no = self.piece_counter
            eid = "q%(qc)d_%(no)d" % locals()
            aname = element.attrib.get('nazwa', None)
            if self.options['single']:
                return u"""
<li class="question-piece" data-qc="%(qc)d" data-no="%(no)d" data-name="%(aname)s">
<input type="radio" name="q%(qc)d" id="%(eid)s" value="%(aname)s" />
<label for="%(eid)s">
                """ % locals(), u"</label></li>"
            else:
                return u"""
<li class="question-piece" data-qc="%(qc)d" data-no="%(no)d" data-name="%(aname)s">
<input type="checkbox" name="%(eid)s" id="%(eid)s" />
<label for="%(eid)s">
""" % locals(), u"</label></li>"

        else:
            return super(Wybor, self).handle_punkt(element)


class Uporzadkuj(Exercise):
    INSTRUCTION = u"Kliknij wybraną odpowiedź i przeciągnij w nowe miejsce."

    def handle_pytanie(self, element):
        """
Overrides the returned content default handle_pytanie
        """
        # we ignore the result, returning our own
        super(Uporzadkuj, self).handle_pytanie(element)
        order_items = element.xpath(".//punkt/@rozw")

        return u"""<div class="question" data-original="%s" data-no="%s">""" % \
            (','.join(order_items), self.question_counter), \
            u"""</div>"""

    def handle_punkt(self, element):
        return """<li class="question-piece" data-pos="%(rozw)s">""" \
            % element.attrib,\
            "</li>"


class Luki(Exercise):
    INSTRUCTION = u"Przeciągnij odpowiedzi i upuść w wybranym polu."
    def find_pieces(self, question):
        return question.xpath(".//luka")

    def solution_html(self, piece):
        piece = deepcopy(piece)
        piece.tail = None
        sub = EduModule()
        return sub.generate(piece)

    def handle_pytanie(self, element):
        qpre, qpost = super(Luki, self).handle_pytanie(element)

        luki = list(enumerate(self.find_pieces(element)))
        luki_html = ""
        i = 0
        random.shuffle(luki)
        for (i, luka) in luki:
            i += 1
            luka_html = self.solution_html(luka)
            luki_html += u'<span class="draggable question-piece" data-no="%d">%s</span>' % (i, luka_html)
        self.words_html = '<div class="words">%s</div>' % luki_html

        return qpre, qpost

    def handle_opis(self, element):
        return '', self.words_html

    def handle_luka(self, element):
        self.piece_counter += 1
        return '<span class="placeholder" data-solution="%d"></span>' % self.piece_counter


class Zastap(Luki):
    INSTRUCTION = u"Przeciągnij odpowiedzi i upuść je na słowie lub wyrażeniu, które chcesz zastąpić."

    def find_pieces(self, question):
        return question.xpath(".//zastap")

    def solution_html(self, piece):
        return piece.attrib.get('rozw', '')

    def handle_zastap(self, element):
        self.piece_counter += 1
        return '<span class="placeholder zastap question-piece" data-solution="%d">' \
            % self.piece_counter, '</span>'


class Przyporzadkuj(Exercise):
    INSTRUCTION = [u"Przeciągnij odpowiedzi i upuść w wybranym polu.",
                   u"Kliknij numer odpowiedzi, przeciągnij i upuść w wybranym polu."]

    def get_instruction(self):
        if not self.instruction_printed:
            self.instruction_printed = True
            return u'<span class="instruction">%s</span>' % self.INSTRUCTION[self.options['handles'] and 1 or 0]
        else:
            return ""

    def handle_cwiczenie(self, element):
        pre, post = super(Przyporzadkuj, self).handle_cwiczenie(element)
        lista_with_handles = element.xpath(".//*[@uchwyty]")
        if lista_with_handles:
            self.options = {'handles': True}
        return pre, post

    def handle_pytanie(self, element):
        pre, post = super(Przyporzadkuj, self).handle_pytanie(element)
        minimum = element.attrib.get("min", None)
        if minimum:
            self.options = {"min": int(minimum)}
        return pre, post

    def handle_lista(self, lista):
        if 'nazwa' in lista.attrib:
            attrs = {
                'data-name': lista.attrib['nazwa'],
                'class': 'predicate'
            }
            self.options = {'predicate': True}
        elif 'cel' in lista.attrib:
            attrs = {
                'data-target': lista.attrib['cel'],
                'class': 'subject'
            }
            self.options = {'subject': True}
        else:
            attrs = {}
        pre, post = super(Przyporzadkuj, self).handle_lista(lista, attrs)
        return pre, post + '<br class="clr"/>'

    def handle_punkt(self, element):
        if self.options['subject']:
            self.piece_counter += 1
            if self.options['handles']:
                return '<li><span data-solution="%s" data-no="%s" class="question-piece draggable handle add-li">%s</span>' % (element.attrib.get('rozw', ''), self.piece_counter, self.piece_counter), '</li>'
            else:
                return '<li data-solution="%s" data-no="%s" class="question-piece draggable">' % (element.attrib.get('rozw', ''), self.piece_counter), '</li>'

        elif self.options['predicate']:
            if self.options['min']:
                placeholders = u'<li class="placeholder"></li>' * self.options['min']
            else:
                placeholders = u'<li class="placeholder multiple"></li>'
            return '<li data-predicate="%s">' % element.attrib.get('nazwa', ''), '<ul class="subjects">' + placeholders + '</ul></li>'

        else:
            return super(Przyporzadkuj, self).handle_punkt(element)


class PrawdaFalsz(Exercise):
    def handle_punkt(self, element):
        if 'rozw' in element.attrib:
            return u'''<li data-solution="%s" class="question-piece">
            <span class="buttons">
            <a href="#" data-value="true" class="true">Prawda</a>
            <a href="#" data-value="false" class="false">Fałsz</a>
        </span>''' % {'prawda': 'true', 'falsz': 'false'}[element.attrib['rozw']], '</li>'
        else:
            return super(PrawdaFalsz, self).handle_punkt(element)


class EduModuleFormat(Format):
    PRIMARY_MATERIAL_FORMATS = ('pdf', 'odt')

    class MaterialNotFound(BaseException):
        pass

    def __init__(self, wldoc, **kwargs):
        super(EduModuleFormat, self).__init__(wldoc, **kwargs)

    def build(self):
        # Sort materials by slug.
        self.materials_by_slug = {}
        for name, att in self.wldoc.source.attachments.items():
            parts = name.rsplit('.', 1)
            if len(parts) == 1:
                continue
            slug, ext = parts
            if slug not in self.materials_by_slug:
                self.materials_by_slug[slug] = {}
            self.materials_by_slug[slug][ext] = att

        edumod = EduModule({'provider': self.wldoc.provider, 'urlmapper': self, 'wldoc': self.wldoc})

        html = edumod.generate(self.wldoc.edoc.getroot())

        return IOFile.from_string(html.encode('utf-8'))

    def materials(self, slug):
        """Returns a list of pairs: (ext, iofile)."""
        order = dict(reversed(k) for k in enumerate(self.PRIMARY_MATERIAL_FORMATS))
        mats = self.materials_by_slug.get(slug, {}).items()
        if not mats:
            print "!! Material missing: '%s'" % slug
        return sorted(mats, key=lambda (x, y): order.get(x, x))

    def url_for_material(self, slug, fmt):
        return "%s.%s" % (slug, fmt)

    def url_for_image(self, slug, fmt, width=None):
        return self.url_for_material(self, slug, fmt)


def transform(wldoc, stylesheet='edumed', options=None, flags=None):
    """Transforms the WL document to XHTML.

    If output_filename is None, returns an XML,
    otherwise returns True if file has been written,False if it hasn't.
    File won't be written if it has no content.
    """
    edumodfor = EduModuleFormat(wldoc)
    return edumodfor.build()
