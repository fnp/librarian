# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from lxml import etree
from librarian import OutputFile, RDFNS, DCNS
from xmlutils import Xmill, tag, tagged, ifoption
import random 

class EduModule(Xmill):
    def __init__(self, *args):
        super(EduModule, self).__init__(*args)
        self.activity_counter = 0

    def handle_powiesc(self, element):
        return u"""
<div class="module" id="book-text">
 <span class="teacher-toggle">
  <input type="checkbox" name="teacher-toggle" id="teacher-toggle"/>
  <label for="teacher-toggle">Pokaż treść dla nauczyciela</label>
 </span>

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
        submill = EduModule()

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

    handle_opis = ifoption(activity=False)(tag('div', 'description'))
    handle_wskazowki = ifoption(activity=False)(tag('div', ('hints', 'teacher')))
    
    @ifoption(activity=False)
    @tagged('div', 'materials')
    def handle_pomoce(self, _):
        return "Pomoce: ", ""
    
    def handle_czas(self, *_):
        return

    def handle_forma(self, *_):
        return
            
    def handle_cwiczenie(self, element):
        excercise_handlers = {
            'wybor': Wybor,
            'uporzadkuj': Uporzadkuj,
            'luki': Luki,
            'zastap': Zastap,
            'przyporzadkuj': Przyporzadkuj,
            'prawdafalsz': PrawdaFalsz
            }
        
        typ = element.attrib['typ']
        handler = excercise_handlers[typ](self.options)
        return handler.generate(element)

    # Lists
    def handle_lista(self, element, attrs={}):
        ltype = element.attrib.get('typ', 'punkt')
        if ltype == 'slowniczek':
            self.options = {'slowniczek': True}
            return '<div class="slowniczek">', '</div>'
### robie teraz punkty wyboru
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

    def handle_rdf__RDF(self, _):
        # ustal w opcjach  rzeczy :D
        return 


class Excercise(EduModule):
    def __init__(self, *args, **kw):
        self.question_counter = 0
        super(Excercise, self).__init__(*args, **kw)

    def handle_rozw_kom(self, element):
        return None

    def handle_cwiczenie(self, element):
        self.options = {'excercise': element.attrib['typ']}
        self.question_counter = 0
        self.piece_counter = 0

        pre = u"""
<div class="excercise %(typ)s" data-type="%(typ)s">
<form action="#" method="POST">
""" % element.attrib
        post = u"""
<div class="buttons">
<span class="message"></span>
<input type="button" class="check" value="sprawdź"/>
<input type="button" class="solutions" value="pokaż rozwiązanie"/>
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
        self.question_counter += 1
        self.piece_counter = 0
        solution = element.attrib.get('rozw', None)
        if solution: solution_s = ' data-solution="%s"' % solution
        else: solution_s = ''

        return '<div class="question" data-no="%d" %s>' %\
            (self.question_counter, solution_s), \
    "</div>"


class Wybor(Excercise):
    def handle_punkt(self, element):
        if self.options['excercise'] and element.attrib.get('nazwa', None):
            qc = self.question_counter
            self.piece_counter += 1
            no = self.piece_counter
            eid = "q%(qc)d_%(no)d" % locals()
            aname = element.attrib.get('nazwa', None)
            return u"""
<li class="question-piece" data-qc="%(qc)d" data-no="%(no)d" data-name="%(aname)s">
<input type="checkbox" name="" id="%(eid)s" />
<label for="%(eid)s">
""" % locals(), u"</label></li>"

        else:
            return super(Wybor, self).handle_punkt(element)


class Uporzadkuj(Excercise):
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


class Luki(Excercise):
    def handle_pytanie(self, element):
        qpre, qpost = super(Luki, self).handle_pytanie(element)

        luki = list(enumerate(element.xpath("//luka")))
        luki_html = ""
        i = 0
        random.shuffle(luki)
        for (i, luka) in luki:
            i += 1
            luka_html = luka.text + \
                ''.join([etree.tostring(n, encoding=unicode) for n in luka])
            luki_html += u'<span class="draggable question-piece" data-no="%d">%s</span>' % (i, luka_html)
        self.words_html = '<div class="words">%s</div>' % luki_html
        
        return qpre, qpost

    def handle_opis(self, element):
        pre, post = super(Luki, self).handle_opis(element)
        return pre, self.words_html + post
                
    def handle_luka(self, element):
        self.piece_counter += 1
        return '<span class="placeholder" data-solution="%d"></span>' % self.piece_counter


class Zastap(Excercise):
    def handle_zastap(self, element):
        return '<span class="zastap question-piece" data-solution="%(rozw)s">' % element.attrib, '</span>'


class Przyporzadkuj(Excercise):
    def handle_lista(self, lista):
        print "in lista %s %s" % (lista.attrib, self.options)
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
        self.piece_counter += 1
        print "in punkt %s %s" % (element.attrib, self.options)

        if self.options['subject']:
            return '<li data-solution="%s" data-no="%s" class="question-piece draggable">' % (element.attrib['rozw'], self.piece_counter), '</li>'
        
        elif self.options['predicate']:
            print etree.tostring(element, encoding=unicode)
            placeholders = u'<li class="placeholder multiple"/>'
            return '<li data-predicate="%(nazwa)s">' % element.attrib, '<ul class="subjects">' + placeholders + '</ul></li>'
        
        else:
            return super(Przyporzadkuj, self).handle_punkt(element)


class PrawdaFalsz(Excercise):
    def handle_punkt(self, element):
        if 'rozw' in element.attrib:
            return u'''<li data-solution="%s" class="question-piece">
            <span class="buttons">
            <a href="#" data-value="true" class="true">Prawda</a>
            <a href="#" data-value="false" class="false">Fałsz</a>
        </span>''' % {'prawda': 'true', 'falsz': 'false'}[element.attrib['rozw']], '</li>'
        else:
            return super(PrawdaFalsz, self).handle_punkt(element)


def transform(wldoc, stylesheet='edumed', options=None, flags=None):
    """Transforms the WL document to XHTML.

    If output_filename is None, returns an XML,
    otherwise returns True if file has been written,False if it hasn't.
    File won't be written if it has no content.
    """
    edumod = EduModule(options)
#    from pdb import set_trace; set_trace()
    html = edumod.generate(wldoc.edoc.getroot())

    return OutputFile.from_string(html.encode('utf-8'))
