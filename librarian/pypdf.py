# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
"""PDF creation library.

Creates one big XML from the book and its children, converts it to LaTeX
with TeXML, then runs it by XeLaTeX.

"""
from copy import deepcopy
import os.path
import shutil
import re
import random
from urllib2 import urlopen

from lxml import etree

from xmlutils import Xmill, ifoption, tag_open_close
from librarian import DCNS, get_resource, IOFile
from librarian import functions
from pdf import PDFFormat, substitute_hyphens, fix_hanging


def escape(really):
    def deco(f):
        def _wrap(*args, **kw):
            value = f(*args, **kw)

            prefix = (u'<TeXML escape="%d">' % (1 if really else 0))
            postfix = u'</TeXML>'
            if isinstance(value, list):
                import pdb
                pdb.set_trace()
            if isinstance(value, tuple):
                return prefix + value[0], value[1] + postfix
            else:
                return prefix + value + postfix
        return _wrap
    return deco


def cmd(name, parms=None):
    def wrap(self, element=None):
        pre, post = tag_open_close('cmd', name=name)

        if parms:
            for parm in parms:
                e = etree.Element("parm")
                e.text = parm
                pre += etree.tostring(e)
        if element is not None:
            pre += "<parm>"
            post = "</parm>" + post
            return pre, post
        else:
            return pre + post
    return wrap


def mark_alien_characters(text):
    text = re.sub(ur"([\u0400-\u04ff]+)", ur"<alien>\1</alien>", text)
    return text


class EduModule(Xmill):
    def __init__(self, options=None, state=None):
        super(EduModule, self).__init__(options, state)
        self.activity_counter = 0
        self.activity_last = None
        self.exercise_counter = 0

        def swap_endlines(txt):
            if self.options['strofa']:
                txt = txt.replace("/\n", '<ctrl ch="\\"/>')
            return txt
        self.register_text_filter(swap_endlines)
        self.register_text_filter(functions.substitute_entities)
        self.register_text_filter(mark_alien_characters)

    def get_dc(self, element, dc_field, single=False):
        values = map(lambda t: t.text, element.xpath("//dc:%s" % dc_field, namespaces={'dc': DCNS.uri}))
        if single:
            return values[0] if len(values) else ''
        return values

    def handle_rdf__RDF(self, _):
        """skip metadata in generation"""
        return

    @escape(True)
    def get_rightsinfo(self, element):
        rights_lic = self.get_dc(element, 'rights.license', True)
        return u'<cmd name="rightsinfostr">' + (u'<opt>%s</opt>' % rights_lic if rights_lic else '') + \
            u'<parm>%s</parm>' % self.get_dc(element, 'rights', True) + \
            u'</cmd>'

    @escape(True)
    def get_authors(self, element, which=None):
        dc = self.options['wldoc'].book_info
        if which is None:
            authors = dc.authors_textbook + \
                dc.authors_scenario + \
                dc.authors_expert
        else:
            authors = getattr(dc, "authors_%s" % which)
        return u', '.join(author.readable() for author in authors if author)

    @escape(True)
    def get_title(self, element):
        return self.get_dc(element, 'title', True)

    @escape(True)
    def get_description(self, element):
        desc = self.get_dc(element, 'description', single=True)
        if not desc:
            print '!! no description'
        return desc

    @escape(True)
    def get_curriculum(self, element):
        identifiers = self.get_dc(element, 'subject.curriculum')
        if not identifiers:
            return ''
        try:
            from curriculum.templatetags.curriculum_tags import curriculum
            curr_elements = curriculum(identifiers)
        except ImportError:
            curr_elements = {'identifiers': identifiers}
        items = ['Podstawa programowa:']
        newline = '<ctrl ch="\\"/>\n'
        if 'currset' in curr_elements:
            for (course, level), types in curr_elements['currset'].iteritems():
                lines = [u'%s, %s poziom edukacyjny' % (course, level)]
                for type, currs in types.iteritems():
                    lines.append(type)
                    lines += [curr.title for curr in currs]
                items.append(newline.join(lines))
        else:
            items += identifiers
        return '\n<cmd name="vspace"><parm>.6em</parm></cmd>\n'.join(
            '<cmd name="akap"><parm>%s</parm></cmd>' % item for item in items)

    def handle_utwor(self, element):
        lines = [
            u'''
                <TeXML xmlns="http://getfo.sourceforge.net/texml/ns1">
                <TeXML escape="0">
                \\documentclass[%s]{wl}
                \\usepackage{style}''' % self.options['customization_str'],
            self.options['has_cover'] and '\usepackage{makecover}',
            (self.options['morefloats'] == 'new' and '\usepackage[maxfloats=64]{morefloats}') or
            (self.options['morefloats'] == 'old' and '\usepackage{morefloats}') or
            (self.options['morefloats'] == 'none' and
                u'''\\IfFileExists{morefloats.sty}{
                \\usepackage{morefloats}
                }{}'''),
            u'''\\def\\authors{%s}''' % self.get_authors(element),
            u'''\\def\\authorsexpert{%s}''' % self.get_authors(element, 'expert'),
            u'''\\def\\authorsscenario{%s}''' % self.get_authors(element, 'scenario'),
            u'''\\def\\authorstextbook{%s}''' % self.get_authors(element, 'textbook'),
            u'''\\def\\description{%s}''' % self.get_description(element),

            u'''\\author{\\authors}''',
            u'''\\title{%s}''' % self.get_title(element),
            u'''\\def\\bookurl{%s}''' % self.options['wldoc'].book_info.url.canonical(),
            u'''\\def\\rightsinfo{%s}''' % self.get_rightsinfo(element),
            u'''\\def\\curriculum{%s}''' % self.get_curriculum(element),
            u'</TeXML>'
        ]

        return u"".join(filter(None, lines)), u'</TeXML>'

    @escape(True)
    def handle_powiesc(self, element):
        return u"""
    <env name="document">
    <cmd name="maketitle"/>
    """, """<cmd name="editorialsection" /></env>"""

    @escape(True)
    def handle_texcommand(self, element):
        cmd = functions.texcommand(element.tag)
        return u'<TeXML escape="1"><cmd name="%s"><parm>' % cmd, u'</parm></cmd></TeXML>'

    handle_akap = \
        handle_akap_cd = \
        handle_akap_dialog = \
        handle_autor_utworu = \
        handle_dedykacja = \
        handle_didaskalia = \
        handle_didask_tekst = \
        handle_dlugi_cytat = \
        handle_dzielo_nadrzedne = \
        handle_lista_osoba = \
        handle_mat = \
        handle_miejsce_czas = \
        handle_motto = \
        handle_motto_podpis = \
        handle_naglowek_akt = \
        handle_naglowek_czesc = \
        handle_naglowek_listy = \
        handle_naglowek_osoba = \
        handle_naglowek_scena = \
        handle_nazwa_utworu = \
        handle_nota = \
        handle_osoba = \
        handle_pa = \
        handle_pe = \
        handle_podtytul = \
        handle_poezja_cyt = \
        handle_pr = \
        handle_pt = \
        handle_sekcja_asterysk = \
        handle_sekcja_swiatlo = \
        handle_separator_linia = \
        handle_slowo_obce = \
        handle_srodtytul = \
        handle_tytul_dziela = \
        handle_wyroznienie = \
        handle_dywiz = \
        handle_texcommand

    def handle_naglowek_rozdzial(self, element):
        if not self.options['teacher']:
            if element.text.startswith((u'Wiedza', u'Zadania', u'Słowniczek', u'Dla ucznia')):
                self.state['mute'] = False
            else:
                self.state['mute'] = True
                return None
        return self.handle_texcommand(element)
    handle_naglowek_rozdzial.unmuter = True

    def handle_naglowek_podrozdzial(self, element):
        self.activity_counter = 0
        if not self.options['teacher']:
            if element.text.startswith(u'Dla ucznia'):
                self.state['mute'] = False
                return None
            elif element.text.startswith(u'Dla nauczyciela'):
                self.state['mute'] = True
                return None
            elif self.state['mute']:
                return None
        return self.handle_texcommand(element)
    handle_naglowek_podrozdzial.unmuter = True

    def handle_uwaga(self, _e):
        return None

    def handle_extra(self, _e):
        return None

    def handle_nbsp(self, _e):
        return '<spec cat="tilde" />'

    _handle_strofa = cmd("strofa")

    def handle_strofa(self, element):
        self.options = {'strofa': True}
        return self._handle_strofa(element)

    def handle_aktywnosc(self, element):
        self.activity_counter += 1
        self.options = {
            'activity': True,
            'activity_counter': self.activity_counter,
            'sub_gen': True,
        }
        submill = EduModule(self.options, self.state)

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

        czas = ''.join(element.xpath('czas/text()'))

        counter = self.activity_counter

        if element.getnext().tag == 'aktywnosc' or (len(self.activity_last) and self.activity_last.getnext() == element):
            counter_tex = """<cmd name="activitycounter"><parm>%(counter)d.</parm></cmd>""" % locals()
        else:
            counter_tex = ''

        self.activity_last = element

        return u"""
<cmd name="noindent" />
%(counter_tex)s
<cmd name="activityinfo"><parm>
 <cmd name="activitytime"><parm>%(czas)s</parm></cmd>
 <cmd name="activityform"><parm>%(forma)s</parm></cmd>
 <cmd name="activitytools"><parm>%(pomoce)s</parm></cmd>
</parm></cmd>


%(opis)s

%(wskazowki)s
""" % locals()

    handle_opis = ifoption(sub_gen=True)(lambda s, e: ('', ''))
    handle_wskazowki = ifoption(sub_gen=True)(lambda s, e: ('', ''))

    @ifoption(sub_gen=True)
    def handle_pomoce(self, _):
        return "Pomoce: ", ""

    def handle_czas(self, *_):
        return

    def handle_forma(self, *_):
        return

    def handle_lista(self, element, attrs=None):
        ltype = element.attrib.get('typ', 'punkt')
        if not element.findall("punkt"):
            if ltype == 'czytelnia':
                return 'W przygotowaniu.'
            else:
                return None
        if ltype == 'slowniczek':
            surl = element.attrib.get('src', None)
            if surl is None:
                # print '** missing src on <slowniczek>, setting default'
                surl = 'http://edukacjamedialna.edu.pl/lekcje/slowniczek/'
            sxml = etree.fromstring(self.options['wldoc'].provider.by_uri(surl).get_string())
            self.options = {'slowniczek': True, 'slowniczek_xml': sxml}

        listcmd = {
            'num': 'enumerate',
            'punkt': 'itemize',
            'alfa': 'itemize',
            'slowniczek': 'itemize',
            'czytelnia': 'itemize'
        }[ltype]

        return u'<env name="%s">' % listcmd, u'</env>'

    def handle_punkt(self, element):
        return '<cmd name="item"/>', ''

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
        if typ not in exercise_handlers:
            return '(no handler)'
        self.options = {'exercise_counter': self.exercise_counter}
        handler = exercise_handlers[typ](self.options, self.state)
        return handler.generate(element)

    # XXX this is copied from pyhtml.py, except for return and
    # should be refactored for no code duplication
    def handle_definiendum(self, element):
        nxt = element.getnext()
        definiens_s = ''

        # let's pull definiens from another document
        if self.options['slowniczek_xml'] is not None and (nxt is None or nxt.tag != 'definiens'):
            sxml = self.options['slowniczek_xml']
            assert element.text != ''
            if "'" in (element.text or ''):
                defloc = sxml.xpath("//definiendum[text()=\"%s\"]" % (element.text or '').strip())
            else:
                defloc = sxml.xpath("//definiendum[text()='%s']" % (element.text or '').strip())
            if defloc:
                definiens = defloc[0].getnext()
                if definiens.tag == 'definiens':
                    subgen = EduModule(self.options, self.state)
                    definiens_s = subgen.generate(definiens)

        return u'<cmd name="textbf"><parm>', u"</parm></cmd>: " + definiens_s

    def handle_definiens(self, element):
        return u"", u""

    def handle_podpis(self, element):
        return u"""<env name="figure">""", u"</env>"

    def handle_tabela(self, element):
        max_col = 0
        for w in element.xpath("wiersz"):
            ks = w.xpath("kol")
            if max_col < len(ks):
                max_col = len(ks)
        self.options = {'columnts': max_col}
        # styling:
        #     has_frames = int(element.attrib.get("ramki", "0"))
        #     if has_frames: frames_c = "framed"
        #     else: frames_c = ""
        #     return u"""<table class="%s">""" % frames_c, u"</table>"
        return u'''
<cmd name="begin"><parm>tabular</parm><parm>%s</parm></cmd>
    ''' % ('l' * max_col), u'''<cmd name="end"><parm>tabular</parm></cmd>'''

    @escape(True)
    def handle_wiersz(self, element):
        return u"", u'<ctrl ch="\\"/>'

    @escape(True)
    def handle_kol(self, element):
        if element.getnext() is not None:
            return u"", u'<spec cat="align" />'
        return u"", u""

    def handle_link(self, element):
        if element.attrib.get('url'):
            url = element.attrib.get('url')
            if url == element.text:
                return cmd('url')(self, element)
            else:
                return cmd('href', parms=[element.attrib['url']])(self, element)
        else:
            return cmd('emph')(self, element)

    def handle_obraz(self, element):
        frmt = self.options['format']
        name = element.attrib.get('nazwa', '').strip()
        image = frmt.get_image(name.strip())
        name = image.get_filename().rsplit('/', 1)[-1]
        img_path = "obraz/%s" % name.replace("_", "")
        frmt.attachments[img_path] = image
        return cmd("obraz", parms=[img_path])(self)

    def handle_video(self, element):
        url = element.attrib.get('url')
        if not url:
            print '!! <video> missing url'
            return
        m = re.match(r'(?:https?://)?(?:www.)?youtube.com/watch\?(?:.*&)?v=([^&]+)(?:$|&)', url)
        if not m:
            print '!! unknown <video> url scheme:', url
            return
        name = m.group(1)
        thumb = IOFile.from_string(urlopen("http://img.youtube.com/vi/%s/0.jpg" % name).read())
        img_path = "video/%s.jpg" % name.replace("_", "")
        self.options['format'].attachments[img_path] = thumb
        canon_url = "https://www.youtube.com/watch?v=%s" % name
        return cmd("video", parms=[img_path, canon_url])(self)


class Exercise(EduModule):
    def __init__(self, *args, **kw):
        self.question_counter = 0
        super(Exercise, self).__init__(*args, **kw)
        self.piece_counter = None

    handle_rozw_kom = ifoption(teacher=True)(cmd('akap'))

    def handle_cwiczenie(self, element):
        self.options = {
            'exercise': element.attrib['typ'],
            'sub_gen': True,
        }
        self.question_counter = 0
        self.piece_counter = 0

        header = etree.Element("parm")
        header_cmd = etree.Element("cmd", name="naglowekpodrozdzial")
        header_cmd.append(header)
        header.text = u"Zadanie %d." % self.options['exercise_counter']

        pre = etree.tostring(header_cmd, encoding=unicode)
        post = u""
        # Add a single <pytanie> tag if it's not there
        if not element.xpath(".//pytanie"):
            qpre, qpost = self.handle_pytanie(element)
            pre += qpre
            post = qpost + post
        return pre, post

    def handle_pytanie(self, element):
        """This will handle <cwiczenie> element, when there is no <pytanie>
        """
        self.question_counter += 1
        self.piece_counter = 0
        pre = post = u""
        if self.options['teacher'] and element.attrib.get('rozw'):
            post += u" [rozwiązanie: %s]" % element.attrib.get('rozw')
        return pre, post

    def handle_punkt(self, element):
        pre, post = super(Exercise, self).handle_punkt(element)
        if self.options['teacher'] and element.attrib.get('rozw'):
            post += u" [rozwiązanie: %s]" % element.attrib.get('rozw')
        return pre, post

    def solution_header(self):
        par = etree.Element("cmd", name="par")
        parm = etree.Element("parm")
        parm.text = u"Rozwiązanie:"
        par.append(parm)
        return etree.tostring(par)

    def explicit_solution(self):
        if self.options['solution']:
            par = etree.Element("cmd", name="par")
            parm = etree.Element("parm")
            parm.text = self.options['solution']
            par.append(parm)
            return self.solution_header() + etree.tostring(par)


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
            for n in choices:
                uniq.add(n.attrib.get('nazwa', ''))
            if len(choices) != len(uniq):
                is_single_choice = False
                break

        self.options = {'single': is_single_choice}
        return pre, post

    def handle_punkt(self, element):
        if self.options['exercise'] and element.attrib.get('nazwa', None):
            cmd = 'radio' if self.options['single'] else 'checkbox'
            return u'<cmd name="%s"/>' % cmd, ''
        else:
            return super(Wybor, self).handle_punkt(element)


class Uporzadkuj(Exercise):
    def handle_pytanie(self, element):
        order_items = element.xpath(".//punkt/@rozw")
        return super(Uporzadkuj, self).handle_pytanie(element)


class Przyporzadkuj(Exercise):
    def handle_lista(self, lista):
        header = etree.Element("parm")
        header_cmd = etree.Element("cmd", name="par")
        header_cmd.append(header)
        if 'nazwa' in lista.attrib:
            header.text = u"Kategorie:"
        elif 'cel' in lista.attrib:
            header.text = u"Elementy do przyporządkowania:"
        else:
            header.text = u"Lista:"
        pre, post = super(Przyporzadkuj, self).handle_lista(lista)
        pre = etree.tostring(header_cmd, encoding=unicode) + pre
        return pre, post


class Luki(Exercise):
    def find_pieces(self, question):
        return question.xpath(".//luka")

    def solution(self, piece):
        piece = deepcopy(piece)
        piece.tail = None
        sub = EduModule()
        return sub.generate(piece)

    def handle_pytanie(self, element):
        qpre, qpost = super(Luki, self).handle_pytanie(element)

        luki = self.find_pieces(element)
        random.shuffle(luki)
        self.words = u"<env name='itemize'>%s</env>" % (
            "".join("<cmd name='item'/>%s" % self.solution(luka) for luka in luki)
        )
        return qpre, qpost

    def handle_opis(self, element):
        return '', self.words

    def handle_luka(self, element):
        luka = "_" * 10
        if self.options['teacher']:
            piece = deepcopy(element)
            piece.tail = None
            sub = EduModule()
            text = sub.generate(piece)
            luka += u" [rozwiązanie: %s]" % text
        return luka


class Zastap(Luki):
    def find_pieces(self, question):
        return question.xpath(".//zastap")

    def solution(self, piece):
        return piece.attrib.get('rozw', '')

    def list_header(self):
        return u"Elementy do wstawienia"

    def handle_zastap(self, element):
        piece = deepcopy(element)
        piece.tail = None
        sub = EduModule()
        text = sub.generate(piece)
        if self.options['teacher'] and element.attrib.get('rozw'):
            text += u" [rozwiązanie: %s]" % element.attrib.get('rozw')
        return text


class PrawdaFalsz(Exercise):
    def handle_punkt(self, element):
        pre, post = super(PrawdaFalsz, self).handle_punkt(element)
        if 'rozw' in element.attrib:
            post += u" [Prawda/Fałsz]"
        return pre, post


def fix_lists(tree):
    lists = tree.xpath(".//lista")
    for l in lists:
        if l.text:
            p = l.getprevious()
            if p is not None:
                if p.tail is None:
                    p.tail = ''
                p.tail += l.text
            else:
                p = l.getparent()
                if p.text is None:
                    p.text = ''
                p.text += l.text
            l.text = ''
    return tree


class EduModulePDFFormat(PDFFormat):
    style = get_resource('res/styles/edumed/pdf/edumed.sty')

    def get_texml(self):
        substitute_hyphens(self.wldoc.edoc)
        fix_hanging(self.wldoc.edoc)

        self.attachments = {}
        edumod = EduModule({
            "wldoc": self.wldoc,
            "format": self,
            "teacher": self.customization.get('teacher'),
        })
        texml = edumod.generate(fix_lists(self.wldoc.edoc.getroot())).encode('utf-8')

        open("/tmp/texml.xml", "w").write(texml)
        return texml

    def get_tex_dir(self):
        temp = super(EduModulePDFFormat, self).get_tex_dir()
        shutil.copy(get_resource('res/styles/edumed/logo.png'), temp)
        for name, iofile in self.attachments.items():
            iofile.save_as(os.path.join(temp, name))
        return temp

    def get_image(self, name):
        return self.wldoc.source.attachments[name]
