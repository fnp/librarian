# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
"""PDF creation library.

Creates one big XML from the book and its children, converts it to LaTeX
with TeXML, then runs it by XeLaTeX.

"""
from __future__ import with_statement
import os
import os.path
import shutil
from StringIO import StringIO
from tempfile import mkdtemp, NamedTemporaryFile
import re
from copy import deepcopy
from subprocess import call, PIPE

from Texml.processor import process
from lxml import etree
from lxml.etree import XMLSyntaxError, XSLTApplyError

from xmlutils import Xmill, tag, tagged, ifoption
from librarian.dcparser import Person
from librarian.parser import WLDocument
from librarian import ParseError, DCNS, get_resource, IOFile, Format
from librarian import functions
from pdf import PDFFormat


def escape(really):
    def deco(f):
        def _wrap(*args, **kw):
            value = f(*args, **kw)

            prefix = (u'<TeXML escape="%d">' % (really and 1 or 0))
            postfix = u'</TeXML>'
            if isinstance(value, list):
                import pdb; pdb.set_trace()
            if isinstance(value, tuple):
                return prefix + value[0], value[1] + postfix
            else:
                return prefix + value + postfix
        return _wrap
    return deco


def cmd(name, pass_text=False):
    def wrap(self, element):
        pre = u'<cmd name="%s">' % name

        if pass_text:
            pre += "<parm>%s</parm>" % element.text
            return pre + '</cmd>'
        else:
            return pre, '</cmd>'
    return wrap


def mark_alien_characters(text):
    text = re.sub(ur"([\u0400-\u04ff]+)", ur"<alien>\1</alien>", text)
    return text


class EduModule(Xmill):
    def __init__(self, options=None):
        super(EduModule, self).__init__(options)
        self.activity_counter = 0
        self.register_text_filter(functions.substitute_entities)
        self.register_text_filter(mark_alien_characters)

    def get_dc(self, element, dc_field, single=False):
        values = map(lambda t: t.text, element.xpath("//dc:%s" % dc_field, namespaces={'dc': DCNS.uri}))
        if single:
            return values[0]
        return values

    def handle_rdf__RDF(self, _):
        "skip metadata in generation"
        return

    @escape(True)
    def get_rightsinfo(self, element):
        rights_lic = self.get_dc(element, 'rights.license', True)
        return u'<cmd name="rightsinfostr">' + \
          (rights_lic and u'<opt>%s</opt>' % rights_lic or '') +\
          u'<parm>%s</parm>' % self.get_dc(element, 'rights', True) +\
          u'</cmd>'

    @escape(True)
    def get_authors(self, element):
        authors = self.get_dc(element, 'creator.expert') + \
          self.get_dc(element, 'creator.scenario') + \
          self.get_dc(element, 'creator.textbook')
        return u', '.join(authors)

    @escape(1)
    def get_title(self, element):
        return self.get_dc(element, 'title', True)

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
    u'''\\author{\\authors}''',
    u'''\\title{%s}''' % self.get_title(element),
    u'''\\def\\bookurl{%s}''' % self.get_dc(element, 'identifier.url', True),
    u'''\\def\\rightsinfo{%s}''' % self.get_rightsinfo(element),
    u'</TeXML>']

        return u"".join(filter(None, lines)), u'</TeXML>'


    handle_naglowek_rozdzial = escape(True)(cmd("naglowekrozdzial", True))
    handle_naglowek_podrozdzial = escape(True)(cmd("naglowekpodrozdzial", True))

    @escape(1)
    def handle_powiesc(self, element):
        return u"""
    <env name="document">
    <cmd name="maketitle"/>
    """, """</env>"""

    handle_autor_utworu = cmd('autorutworu', True)
    handle_nazwa_utworu = cmd('nazwautworu', True)
    handle_dzielo_nadrzedne = cmd('dzielonadrzedne', True)
    handle_podtytul = cmd('podtytul', True)

    handle_akap = handle_akap_dialog = handle_akap_cd = lambda s, e: ("\n", "\n")
    handle_strofa = lambda s, e: ("\n","\n")

    def handle_aktywnosc(self, element):
        self.activity_counter += 1
        self.options = {
            'activity': True,
            'activity_counter': self.activity_counter,
            'sub_gen': True,
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
Czas: %(czas)s min
Forma: %(forma)s
%(pomoce)s

%(counter)d. %(opis)s

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

#     def handle_cwiczenie(self, element):
#         exercise_handlers = {
#             'wybor': Wybor,
#             'uporzadkuj': Uporzadkuj,
#             'luki': Luki,
#             'zastap': Zastap,
#             'przyporzadkuj': Przyporzadkuj,
#             'prawdafalsz': PrawdaFalsz
#             }

#         typ = element.attrib['typ']
#         handler = exercise_handlers[typ](self.options)
#         return handler.generate(element)

#     # Lists
#     def handle_lista(self, element, attrs={}):
#         ltype = element.attrib.get('typ', 'punkt')
#         if ltype == 'slowniczek':
#             surl = element.attrib.get('href', None)
#             sxml = None
#             if surl:
#                 sxml = etree.fromstring(self.options['provider'].by_uri(surl).get_string())
#             self.options = {'slowniczek': True, 'slowniczek_xml': sxml }
#             return '<div class="slowniczek">', '</div>'

#         listtag = {'num': 'ol',
#                'punkt': 'ul',
#                'alfa': 'ul',
#                'czytelnia': 'ul'}[ltype]

#         classes = attrs.get('class', '')
#         if classes: del attrs['class']

#         attrs_s = ' '.join(['%s="%s"' % kv for kv in attrs.items()])
#         if attrs_s: attrs_s = ' ' + attrs_s

#         return '<%s class="lista %s %s"%s>' % (listtag, ltype, classes, attrs_s), '</%s>' % listtag

#     def handle_punkt(self, element):
#         if self.options['slowniczek']:
#             return '<dl>', '</dl>'
#         else:
#             return '<li>', '</li>'

#     def handle_definiendum(self, element):
#         nxt = element.getnext()
#         definiens_s = ''

#         # let's pull definiens from another document
#         if self.options['slowniczek_xml'] and (not nxt or nxt.tag != 'definiens'):
#             sxml = self.options['slowniczek_xml']
#             assert element.text != ''
#             defloc = sxml.xpath("//definiendum[text()='%s']" % element.text)
#             if defloc:
#                 definiens = defloc[0].getnext()
#                 if definiens.tag == 'definiens':
#                     subgen = EduModule(self.options)
#                     definiens_s = subgen.generate(definiens)

#         return u"<dt>", u"</dt>" + definiens_s

#     def handle_definiens(self, element):
#         return u"<dd>", u"</dd>"


#     def handle_podpis(self, element):
#         return u"""<div class="caption">""", u"</div>"

#     def handle_tabela(self, element):
#         has_frames = int(element.attrib.get("ramki", "0"))
#         if has_frames: frames_c = "framed"
#         else: frames_c = ""
#         return u"""<table class="%s">""" % frames_c, u"</table>"

#     def handle_wiersz(self, element):
#         return u"<tr>", u"</tr>"

#     def handle_kol(self, element):
#         return u"<td>", u"</td>"

#     def handle_rdf__RDF(self, _):
#         # ustal w opcjach  rzeczy :D
#         return

#     def handle_link(self, element):
#         if 'material' in element.attrib:
#             formats = re.split(r"[, ]+", element.attrib['format'])
#             fmt_links = []
#             for f in formats:
#                 fmt_links.append(u'<a href="%s">%s</a>' % (self.options['urlmapper'].url_for_material(element.attrib['material'], f), f.upper()))

#             return u"", u' (%s)' % u' '.join(fmt_links)


# class Exercise(EduModule):
#     def __init__(self, *args, **kw):
#         self.question_counter = 0
#         super(Exercise, self).__init__(*args, **kw)

#     def handle_rozw_kom(self, element):
#         return u"""<div style="display:none" class="comment">""", u"""</div>"""

#     def handle_cwiczenie(self, element):
#         self.options = {'exercise': element.attrib['typ']}
#         self.question_counter = 0
#         self.piece_counter = 0

#         pre = u"""
# <div class="exercise %(typ)s" data-type="%(typ)s">
# <form action="#" method="POST">
# """ % element.attrib
#         post = u"""
# <div class="buttons">
# <span class="message"></span>
# <input type="button" class="check" value="sprawdź"/>
# <input type="button" class="retry" style="display:none" value="spróbuj ponownie"/>
# <input type="button" class="solutions" value="pokaż rozwiązanie"/>
# <input type="button" class="reset" value="reset"/>
# </div>
# </form>
# </div>
# """
#         # Add a single <pytanie> tag if it's not there
#         if not element.xpath(".//pytanie"):
#             qpre, qpost = self.handle_pytanie(element)
#             pre = pre + qpre
#             post = qpost + post
#         return pre, post

#     def handle_pytanie(self, element):
#         """This will handle <cwiczenie> element, when there is no <pytanie>
#         """
#         add_class = ""
#         self.question_counter += 1
#         self.piece_counter = 0
#         solution = element.attrib.get('rozw', None)
#         if solution: solution_s = ' data-solution="%s"' % solution
#         else: solution_s = ''

#         handles = element.attrib.get('uchwyty', None)
#         if handles:
#             add_class += ' handles handles-%s' % handles
#             self.options = {'handles': handles}

#         minimum = element.attrib.get('min', None)
#         if minimum: minimum_s = ' data-minimum="%d"' % int(minimum)
#         else: minimum_s = ''

#         return '<div class="question%s" data-no="%d" %s>' %\
#             (add_class, self.question_counter, solution_s + minimum_s), \
#             "</div>"

class EduModulePDFFormat(PDFFormat):
    def get_texml(self):
        edumod = EduModule()
        texml = edumod.generate(self.wldoc.edoc.getroot()).encode('utf-8')

        open("/tmp/texml.xml", "w").write(texml)
        return texml
