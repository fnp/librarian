# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from lxml import etree
from librarian import IOFile, RDFNS, DCNS, Format
from xmlutils import Xmill, tag, tagged, ifoption
from librarian import functions
import re
import random



class EduModule(Xmill):
    def __init__(self, options=None):
        super(EduModule, self).__init__(options)
        self.activity_counter = 0
        self.register_text_filter(lambda t: functions.substitute_entities(None, t))

    def handle_powiesc(self, element):
        return u"""
<div class="module" id="book-text">
<!-- <span class="teacher-toggle">
  <input type="checkbox" name="teacher-toggle" id="teacher-toggle"/>
  <label for="teacher-toggle">Pokaż treść dla nauczyciela</label>
 </span>-->

""", u"</div>"

    handle_autor_utworu = tag("span", "author")
    handle_nazwa_utworu = tag("h1", "title")
    handle_dzielo_nadrzedne = tag("span", "collection")
    handle_podtytul = tag("span", "subtitle")
    handle_naglowek_akt = handle_naglowek_czesc = handle_srodtytul = tag("h2")
    handle_naglowek_scena = handle_naglowek_rozdzial = tag('h3')
    handle_naglowek_osoba = handle_naglowek_podrozdzial = tag('h4')
    handle_akap = handle_akap_dialog = handle_akap_cd = tag('p', 'paragraph')
    handle_strofa = tag('div', 'stanza')

    def handle_aktywnosc(self, element):
        self.activity_counter += 1
        self.options = {
            'activity': True,
            'activity_counter': self.activity_counter
            }
        submill = EduModule(self.options)

        opis = submill.generate(element.xpath('opis')[0])

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
 <div class="text">%(counter)d.
  %(opis)s
  %(wskazowki)s
 </div>
 <div class="info">
  <p>Czas: %(czas)s min</p>
  <p>Forma: %(forma)s</p>
  %(pomoce)s
 </div>
 <div class="clearboth"></div>
</div>
""" % locals()

    handle_opis = ifoption(activity=True)(tag('div', 'description'))
    handle_wskazowki = ifoption(activity=True)(tag('div', ('hints', 'teacher')))

    @ifoption(activity=True)
    @tagged('div', 'materials')
    def handle_pomoce(self, _):
        return "Pomoce: ", ""

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
        handler = exercise_handlers[typ](self.options)
        return handler.generate(element)

    # Lists
    def handle_lista(self, element, attrs={}):
        ltype = element.attrib.get('typ', 'punkt')
        if ltype == 'slowniczek':
            surl = element.attrib.get('href', None)
            sxml = None
            if surl:
                sxml = etree.fromstring(self.options['provider'].by_uri(surl).get_string())
            self.options = {'slowniczek': True, 'slowniczek_xml': sxml }
            return '<div class="slowniczek">', '</div>'

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

        # let's pull definiens from another document
        if self.options['slowniczek_xml'] and (not nxt or nxt.tag != 'definiens'):
            sxml = self.options['slowniczek_xml']
            assert element.text != ''
            defloc = sxml.xpath("//definiendum[text()='%s']" % element.text)
            if defloc:
                definiens = defloc[0].getnext()
                if definiens.tag == 'definiens':
                    subgen = EduModule(self.options)
                    definiens_s = subgen.generate(definiens)

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
        if 'material' in element.attrib:
            formats = re.split(r"[, ]+", element.attrib['format'])
            fmt_links = []
            for f in formats:
                fmt_links.append(u'<a href="%s">%s</a>' % (self.options['urlmapper'].url_for_material(element.attrib['material'], f), f.upper()))

            return u"", u' (%s)' % u' '.join(fmt_links)


class Exercise(EduModule):
    def __init__(self, *args, **kw):
        self.question_counter = 0
        super(Exercise, self).__init__(*args, **kw)

    def handle_rozw_kom(self, element):
        return u"""<div style="display:none" class="comment">""", u"""</div>"""

    def handle_cwiczenie(self, element):
        self.options = {'exercise': element.attrib['typ']}
        self.question_counter = 0
        self.piece_counter = 0

        pre = u"""
<div class="exercise %(typ)s" data-type="%(typ)s">
<form action="#" method="POST">
""" % element.attrib
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


class Wybor(Exercise):
    def handle_cwiczenie(self, element):
        pre, post = super(Wybor, self).handle_cwiczenie(element)
        is_single_choice = True
        for p in element.xpath(".//pytanie"):
            solutions = re.split(r"[, ]+", p.attrib['rozw'])
            if len(solutions) != 1:
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
        return """<li class="question-piece" data-pos="%(rozw)s"/>""" \
            % element.attrib,\
            "</li>"


class Luki(Exercise):
    def find_pieces(self, question):
        return question.xpath("//luka")

    def solution_html(self, piece):
        return piece.text + ''.join(
            [etree.tostring(n, encoding=unicode)
             for n in piece])

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
        pre, post = super(Luki, self).handle_opis(element)
        return pre, self.words_html + post

    def handle_luka(self, element):
        self.piece_counter += 1
        return '<span class="placeholder" data-solution="%d"></span>' % self.piece_counter


class Zastap(Luki):
    def find_pieces(self, question):
        return question.xpath("//zastap")

    def solution_html(self, piece):
        return piece.attrib['rozw']

    def handle_zastap(self, element):
        self.piece_counter += 1
        return '<span class="placeholder zastap question-piece" data-solution="%d">' \
            % self.piece_counter, '</span>'


class Przyporzadkuj(Exercise):
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
            self.options = {'subject': True, 'handles': 'uchwyty' in lista.attrib}
        else:
            attrs = {}
        pre, post = super(Przyporzadkuj, self).handle_lista(lista, attrs)
        return pre, post + '<br class="clr"/>'

    def handle_punkt(self, element):
        if self.options['subject']:
            self.piece_counter += 1
            if self.options['handles']:
                return '<li><span data-solution="%s" data-no="%s" class="question-piece draggable handle">%s</span>' % (element.attrib['rozw'], self.piece_counter, self.piece_counter), '</li>'
            else:
                return '<li data-solution="%s" data-no="%s" class="question-piece draggable">' % (element.attrib['rozw'], self.piece_counter), '</li>'

        elif self.options['predicate']:
            if self.options['min']:
                placeholders = u'<li class="placeholder"/>' * self.options['min']
            else:
                placeholders = u'<li class="placeholder multiple"/>'
            return '<li data-predicate="%(nazwa)s">' % element.attrib, '<ul class="subjects">' + placeholders + '</ul></li>'

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
    def __init__(self, wldoc, **kwargs):
        super(EduModuleFormat, self).__init__(wldoc, **kwargs)

    def build(self):
        edumod = EduModule({'provider': self.wldoc.provider, 'urlmapper': self})

        html = edumod.generate(self.wldoc.edoc.getroot())

        return IOFile.from_string(html.encode('utf-8'))

    def url_for_material(self, slug, fmt=None):
        # No briliant idea for an API here.
        if fmt:
            return "%s.%s" % (slug, fmt)
        return slug


def transform(wldoc, stylesheet='edumed', options=None, flags=None):
    """Transforms the WL document to XHTML.

    If output_filename is None, returns an XML,
    otherwise returns True if file has been written,False if it hasn't.
    File won't be written if it has no content.
    """
    edumodfor = EduModuleFormat(wldoc)
    return edumodfor.build()
