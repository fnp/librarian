# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os
import shutil
from tempfile import mkdtemp, NamedTemporaryFile

from lxml import etree
from subprocess import call

from librarian import IOFile, Format, ParseError, get_resource
from xmlutils import Xmill, tag, tagged, ifoption, tag_open_close
from librarian import functions
import re
import random
from copy import deepcopy

IMAGE_THUMB_WIDTH = 300


class EduModule(Xmill):
    def __init__(self, options=None):
        super(EduModule, self).__init__(options)
        self.activity_counter = 0
        self.activity_last = None
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
        return u"""<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <title>Edukacja medialna</title>
        <link href="weasy.css" rel="stylesheet" type="text/css">
        <meta charset="UTF-8">
    </head>
    <body id="body">        
        <div class="module" id="book-text">
""", u"""
        </div>
    </body>
</html>"""

    handle_autor_utworu = tag("span", "author")
    handle_dzielo_nadrzedne = tag("span", "collection")
    handle_podtytul = tag("span", "subtitle")
    handle_naglowek_akt = handle_naglowek_czesc = handle_srodtytul = tag("h2")
    handle_naglowek_scena = tag('h2')
    handle_naglowek_osoba = tag('h3')
    handle_akap = handle_akap_dialog = handle_akap_cd = tag('p', 'paragraph')

    handle_wyroznienie = tag('em')
    handle_tytul_dziela = tag('em', 'title')
    handle_slowo_obce = tag('em', 'foreign')

    def naglowek_to_anchor(self, naglowek):
        return self.options['urlmapper'].naglowek_to_anchor(naglowek)

    def handle_nazwa_utworu(self, element):
        return "<h1 class='title' id='top'>", "</h1>"

    def handle_naglowek_rozdzial(self, element):
        return tag_open_close("h2", id=self.naglowek_to_anchor(element))

    def handle_naglowek_podrozdzial(self, element):
        self.activity_counter = 0
        if element.text.strip() == u'Przebieg zajęć':
            return tag('h3', 'activities-header')(self, element)
        return tag('h3')(self, element)

    def handle_uwaga(self, _e):
        return None

    def handle_aktywnosc(self, element):
        self.activity_counter += 1
        parity = 'odd' if self.activity_counter % 2 == 1 else 'even'
        if self.activity_counter == 1:
            parity += ' first'
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
        if n:
            wskazowki = submill.generate(n[0])
        else:
            wskazowki = ''

        n = element.xpath('pomoce')
        if n:
            pomoce = submill.generate(n[0])
        else:
            pomoce = ''

        forma = ''.join(element.xpath('forma/text()'))
        get_forma_url = self.options['urlmapper'].get_forma_url
        forms = []
        for form_name in forma.split(','):
            name = form_name.strip()
            url = get_forma_url(name)
            if url:
                forms.append("<a href='%s'>%s</a>" % (url, name))
            else:
                forms.append(name)
        forma = ', '.join(forms)
        if forma:
            forma = '<tr class="infobox kind"><th>Metoda</th><td><p>%s</p></td></tr>' % forma

        czas = ''.join(element.xpath('czas/text()'))
        if czas:
            czas = '<tr class="infobox time"><th>Czas</th><td><p>%s min</p></td></tr>' % czas

        counter = self.activity_counter

        if element.getnext().tag == 'aktywnosc' or (len(self.activity_last) and self.activity_last.getnext() == element):
            counter_html = """<span class="act_counter">%(counter)d.</span>""" % {'counter': counter}
        else:
            counter_html = ''

        self.activity_last = element

        return (
            u"""
<div class="activity %(parity)s">
  <div class="text">
    <div class="description">
    %(counter_html)s
    %(opis)s""" % {'counter_html': counter_html, 'opis': opis, 'parity': parity},
            u"""%(wskazowki)s
    </div>
  </div>
  <table class="info">
    %(czas)s
    %(forma)s
    %(pomoce)s
  </table>
  <div class="clearboth"></div>
</div>
""" % {'wskazowki': wskazowki, 'czas': czas, 'forma': forma, 'pomoce': pomoce})

    handle_opis = ifoption(sub_gen=True)(tag('div', 'desc'))
    handle_wskazowki = ifoption(sub_gen=True)(tag('div', ('hints', 'teacher')))

    @ifoption(sub_gen=True)
    @tagged('tr', 'infobox materials')
    def handle_pomoce(self, _):
        return """<th>Pomoce</th><td>""", "</td>"

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
    def handle_lista(self, element, attrs=None):
        if attrs is None:
            attrs = {}
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
            sxml = etree.fromstring(self.options['provider'].by_uri(surl).get_string())

            self.options = {'slowniczek': True, 'slowniczek_xml': sxml}
            return '<div class="slowniczek"><dl>', '</dl></div>'

        listtag = {
            'num': 'ol',
            'punkt': 'ul',
            'alfa': 'ul',
            'czytelnia': 'ul'}[ltype]

        classes = attrs.get('class', '')
        if classes:
            del attrs['class']

        attrs_s = ' '.join(['%s="%s"' % kv for kv in attrs.items()])
        if attrs_s:
            attrs_s = ' ' + attrs_s

        return '<%s class="lista %s %s"%s>' % (listtag, ltype, classes, attrs_s), '</%s>' % listtag

    def handle_punkt(self, element):
        if self.options['slowniczek']:
            return '', ''
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
            if "'" in (element.text or ''):
                defloc = sxml.xpath("//definiendum[text()=\"%s\"]" % (element.text or '').strip())
            else:
                defloc = sxml.xpath("//definiendum[text()='%s']" % (element.text or '').strip())
            if defloc:
                definiens = defloc[0].getnext()
                if definiens.tag == 'definiens':
                    subgen = EduModule(self.options)
                    definiens_s = subgen.generate(definiens)
            else:
                print ("!! Missing definiendum in source: '%s'" % element.text).encode('utf-8')

        return u"<dt id='%s'>" % self.naglowek_to_anchor(element), u"</dt>" + definiens_s

    def handle_definiens(self, element):
        return u"<dd>", u"</dd>"

    def handle_podpis(self, element):
        return u"""<div class="caption">""", u"</div>"

    def handle_tabela(self, element):
        has_frames = int(element.attrib.get("ramki", "0"))
        frames_c = "framed" if has_frames else ""
        return u"""<table class="%s">""" % frames_c, u"</table>"

    def handle_wiersz(self, element):
        return u"<tr>", u"</tr>"

    def handle_kol(self, element):
        return u"<td>", u"</td>"

    def handle_rdf__RDF(self, _):
        # ustal w opcjach rzeczy :D
        return

    def handle_link(self, element):
        if 'url' in element.attrib:
            return tag('a', href=element.attrib['url'])(self, element)
        elif 'material' in element.attrib:
            material_err = u' [BRAKUJĄCY MATERIAŁ]'
            slug = element.attrib['material']

            def make_url(f):
                return self.options['urlmapper'].url_for_material(slug, f)

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
        format = self.options['urlmapper']
        name = element.attrib.get('nazwa', '').strip()
        if not name:
            print '!! <obraz> missing "nazwa"'
            return
        alt = element.attrib.get('alt', '')
        if not alt:
            print '** <obraz> missing "alt"'
        slug, ext = name.rsplit('.', 1)
        image = format.image(slug, ext)
        name = image.name.rsplit('/', 1)[-1]
        e = etree.Element("a", attrib={"class": "image"})
        e.append(etree.Element("img", attrib={
            "src": name,
            "alt": alt,
            "width": str(IMAGE_THUMB_WIDTH)}))
        format.attachments[name] = self.options['media_root'] + image.name
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
        self.piece_counter = None

    @tagged('div', 'description')
    def handle_opis(self, element):
        return "", self.get_instruction()

    def handle_rozw_kom(self, element):
        return u"""<div style="display:none" class="comment">""", u"""</div>"""

    def extra_attributes(self):
        return {}

    def handle_cwiczenie(self, element):
        self.options = {'exercise': element.attrib['typ']}
        self.question_counter = 0
        self.piece_counter = 0

        extra_attrs = self.extra_attributes()

        pre = u"""
<div class="exercise %(typ)s" data-type="%(typ)s"%(extra_attrs)s>
<h3>Zadanie %(exercies_counter)d</h3>
""" % {
            'exercies_counter': self.options['exercise_counter'],
            'typ': element.attrib['typ'],
            'extra_attrs': ' ' + ' '.join(
                'data-%s="%s"' % item for item in extra_attrs.iteritems()) if extra_attrs else '',
        }
        post = u"""
</div>
"""
        # Add a single <pytanie> tag if it's not there
        if not element.xpath(".//pytanie"):
            qpre, qpost = self.handle_pytanie(element)
            pre += qpre
            post = qpost + post
        return pre, post

    def handle_pytanie(self, element):
        """This will handle <cwiczenie> element, when there is no <pytanie>
        """
        add_class = ""
        self.question_counter += 1
        self.piece_counter = 0
        solution = element.attrib.get('rozw', None)
        solution_s = ' data-solution="%s"' % solution if solution else ''

        handles = element.attrib.get('uchwyty', None)
        if handles:
            add_class += ' handles handles-%s' % handles
            self.options = {'handles': handles}

        minimum = element.attrib.get('min', None)
        minimum_s = ' data-minimum="%d"' % int(minimum) if minimum else ''

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
    def extra_attributes(self):
        return {'subtype': 'single' if self.options['single'] else 'multiple'}

    def handle_cwiczenie(self, element):
        is_single_choice = True
        pytania = element.xpath(".//pytanie")
        if not pytania:
            pytania = [element]
        for p in pytania:
            solutions = p.xpath(".//punkt[@rozw='prawda']")
            if len(solutions) != 1:
                is_single_choice = False
                break

        self.options = {'single': is_single_choice}
        return super(Wybor, self).handle_cwiczenie(element)

    def handle_punkt(self, element):
        if self.options['exercise'] and element.attrib.get('rozw', None):
            qc = self.question_counter
            self.piece_counter += 1
            no = self.piece_counter
            eid = "q%(qc)d_%(no)d" % locals()
            sol = element.attrib.get('rozw', None)
            params = {'qc': qc, 'no': no, 'sol': sol, 'eid': eid}
            if self.options['single']:
                input_tag = u'<input type="radio" name="q%(qc)d" id="%(eid)s" value="%(eid)s" />'
            else:
                input_tag = u'<input type="checkbox" name="%(eid)s" id="%(eid)s" />'
            return (u"""
<li class="question-piece" data-qc="%(qc)d" data-no="%(no)d" data-sol="%(sol)s">
                """ + input_tag + u"""
<label for="%(eid)s">""") % params, u"</label></li>"
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
            if lista.attrib.get('krotkie'):
                self.options = {'short': True}
            self.options = {'subject': True}
        else:
            attrs = {}
        pre, post = super(Przyporzadkuj, self).handle_lista(lista, attrs)
        return pre, post + '<br class="clearboth"/>'

    def handle_punkt(self, element):
        if self.options['subject']:
            self.piece_counter += 1
            if self.options['handles']:
                return (
                    '<li><span data-solution="%s" data-no="%s" '
                    'class="question-piece draggable handle add-li">%s</span>' % (
                        element.attrib.get('rozw', ''),
                        self.piece_counter,
                        self.piece_counter),
                    '</li>')
            else:
                extra_class = ""
                if self.options['short']:
                    extra_class += ' short'
                return '<li data-solution="%s" data-no="%s" class="question-piece draggable%s">' % (
                    element.attrib.get('rozw', ''),
                    self.piece_counter, extra_class), '</li>'

        elif self.options['predicate']:
            if self.options['min']:
                placeholders = u'<li class="placeholder"></li>' * self.options['min']
            else:
                placeholders = u'<li class="placeholder multiple"></li>'
            return (
                '<li data-predicate="%s">' % element.attrib.get('nazwa', ''),
                '<ul class="subjects">' + placeholders + '</ul></li>')

        else:
            return super(Przyporzadkuj, self).handle_punkt(element)


class PrawdaFalsz(Exercise):
    def handle_punkt(self, element):
        if 'rozw' in element.attrib:
            return u'''<li data-solution="%s" class="question-piece">
            <span class="buttons">
                <a data-value="true" class="true">Prawda</a>
                <a data-value="false" class="false">Fałsz</a>
            </span>
            <span class="question-piece-text">''' % {
                'prawda': 'true',
                'falsz': 'false'
            }[element.attrib['rozw']], '</span></li>'
        else:
            return super(PrawdaFalsz, self).handle_punkt(element)


class EduModuleWeasyFormat(Format):
    PRIMARY_MATERIAL_FORMATS = ('pdf', 'odt')

    class MaterialNotFound(BaseException):
        pass

    def __init__(self, wldoc, media_root='', save_html_to=None, **kwargs):
        super(EduModuleWeasyFormat, self).__init__(wldoc, **kwargs)
        self.media_root = media_root
        self.materials_by_slug = None
        self.attachments = {}
        self.save_html_to = save_html_to

    def get_html(self):
        self.attachments = {}
        edumod = EduModule({
            'provider': self.wldoc.provider,
            'urlmapper': self,
            'wldoc': self.wldoc,
            'media_root': self.media_root,
        })
        return edumod.generate(self.wldoc.edoc.getroot())

    def get_weasy_dir(self):
        html = self.get_html()
        temp = mkdtemp('-weasy')
        # Save TeX file
        html_path = os.path.join(temp, 'doc.html')
        with open(html_path, 'w') as fout:
            fout.write(html.encode('utf-8'))
        # Copy style
        weasy_dir = os.path.join(os.path.dirname(__file__), 'weasy')
        for filename in os.listdir(weasy_dir):
            shutil.copy(get_resource('weasy/%s' % filename), temp)
        for name, path in self.attachments.items():
            shutil.copy(path, os.path.join(temp, name))
        return temp

    def get_pdf(self):
        temp = self.get_weasy_dir()
        if self.save_html_to:
            save_path = os.path.join(self.save_html_to, 'weasy-html')
            shutil.rmtree(save_path, ignore_errors=True)
            shutil.copytree(temp, save_path)
        html_path = os.path.join(temp, 'doc.html')
        pdf_path = os.path.join(temp, 'doc.pdf')
        try:
            cwd = os.getcwd()
        except OSError:
            cwd = None
        os.chdir(temp)

        WEASY_COMMAND = '/home/janek/Desktop/weasy-test/bin/weasyprint'

        p = call([WEASY_COMMAND, html_path, pdf_path])
        if p:
            raise ParseError("Error parsing .html file: %s" % html_path)

        if cwd is not None:
            os.chdir(cwd)

        output_file = NamedTemporaryFile(prefix='librarian', suffix='.pdf', delete=False)
        shutil.move(pdf_path, output_file.name)
        # shutil.rmtree(temp)
        return IOFile.from_filename(output_file.name)

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
        return self.get_pdf()

    def materials(self, slug):
        """Returns a list of pairs: (ext, iofile)."""
        order = {pmf: i for (i, pmf) in enumerate(self.PRIMARY_MATERIAL_FORMATS)}
        mats = self.materials_by_slug.get(slug, {}).items()
        if not mats:
            print ("!! Material missing: '%s'" % slug).encode('utf-8')
        return sorted(mats, key=lambda (x, y): order.get(x, x))

    def url_for_material(self, slug, fmt):
        return "%s.%s" % (slug, fmt)

    def url_for_image(self, slug, fmt, width=None):
        return self.url_for_material(slug, fmt)

    def text_to_anchor(self, text):
        return re.sub(r" +", " ", text)

    def naglowek_to_anchor(self, naglowek):
        return self.text_to_anchor(naglowek.text.strip())

    def get_forma_url(self, forma):
        return None

    def get_help_url(self, naglowek):
        return None


def transform(wldoc, stylesheet='edumed', options=None, flags=None, verbose=None):
    """Transforms the WL document to XHTML.

    If output_filename is None, returns an XML,
    otherwise returns True if file has been written,False if it hasn't.
    File won't be written if it has no content.
    """
    edumodfor = EduModuleWeasyFormat(wldoc)
    return edumodfor.build()