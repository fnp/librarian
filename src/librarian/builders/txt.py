# coding: utf-8
from __future__ import unicode_literals

import io
from librarian import OutputFile, get_resource


with io.open(get_resource("res/text/template.txt")) as f:
    TEMPLATE = f.read()


class TxtFragment:
    def __init__(self):
        self.pieces = []
        self.current_margin = 0
        self.starting_block = True

    def push_legacy_margin(self, margin):
        if margin:
            if self.pieces:
                self.pieces[-1] = self.pieces[-1].rstrip(' ')
            self.pieces.append('\r\n' * margin)
            self.current_margin += margin
            self.starting_block = True
        
    def push_margin(self, margin):
        if margin:
            if self.pieces:
                self.pieces[-1] = self.pieces[-1].rstrip(' ')
            if margin > self.current_margin:
                self.pieces.append('\r\n' * (margin - self.current_margin))
                self.current_margin = margin
                self.starting_block = True

    def push_text(self, text, prepared=False):
        if text:
            if self.starting_block and not prepared:
                text = text.lstrip()
            self.pieces.append(text)
            self.current_margin = 0
            if not prepared:
                self.starting_block = False


class TxtBuilder:
    """
    """
    file_extension = "txt"
    identifier = "txt"

    default_license_description = {
        "pol": (
            "Ten utwór nie jest objęty majątkowym prawem autorskim "
            "i znajduje się w domenie publicznej, co oznacza że "
            "możesz go swobodnie wykorzystywać, publikować "
            "i rozpowszechniać. Jeśli utwór opatrzony jest "
            "dodatkowymi materiałami (przypisy, motywy literackie "
            "etc.), które podlegają prawu autorskiemu, to te "
            "dodatkowe materiały udostępnione są na licencji "
            "Creative Commons Uznanie Autorstwa – Na Tych Samych "
            "Warunkach 3.0 PL "
            "(http://creativecommons.org/licenses/by-sa/3.0/)"
        )
    }
    license_description = {
        "pol": "Ten utwór jest udostępniony na licencji {meta.license_description}: \n{meta.license}",
    }

    def __init__(self):
        self.fragments = {
            None: TxtFragment(),
            'header': TxtFragment()
        }
        self.current_fragments = [self.fragments[None]]

    def enter_fragment(self, fragment):
        self.current_fragments.append(self.fragments[fragment])

    def exit_fragment(self):
        self.current_fragments.pop()
        
    def push_text(self, text, prepared=False):
        self.current_fragments[-1].push_text(text, prepared=prepared)

    def push_margin(self, margin):
        self.current_fragments[-1].push_margin(margin)
        
    def push_legacy_margin(self, margin, where=None):
        self.current_fragments[-1].push_legacy_margin(margin)
        
    def build(self, document, raw_text=False, **kwargs):
        document.tree.getroot().txt_build(self)
        meta = document.meta

        self.enter_fragment('header')
        if meta.translators:
            self.push_text("tłum. ")
            self.push_text(
                ", ".join(
                    translator.readable()
                    for translator in meta.translators
                )
            )
            #builder.push_margin(2)
            self.push_legacy_margin(1)

        if meta.isbn_txt:
            #builder.push_margin(2)
            self.push_legacy_margin(1)
            isbn = meta.isbn_txt
            if isbn.startswith(('ISBN-' , 'ISBN ')):
                isbn = isbn[5:]
            self.push_text('ISBN {isbn}'.format(isbn=isbn))
            #builder.push_margin(5)

        #builder.push_margin(4)
        self.push_legacy_margin(1)
        self.exit_fragment()
        
        text = ''.join(self.fragments['header'].pieces) +  ''.join(self.fragments[None].pieces)

        if raw_text:
            result = text
        else:
            if meta.license:
                license_description = self.license_description['pol'].format(meta=meta)
            else:
                license_description = self.default_license_description['pol']

            if meta.source_name:
                source = "\n\nTekst opracowany na podstawie: " + meta.source_name
            else:
                source = ''

            contributors = ', '.join(
                person.readable()
                for person in sorted(set(
                    p for p in (
                        meta.technical_editors + meta.editors
                    ) if p))
            )
            if contributors:
                contributors = (
                    "\n\nOpracowanie redakcyjne i przypisy: %s."
                    % contributors
                )

            funders = ', '.join(meta.funders)
            if funders:
                funders = u"\n\nPublikację wsparli i wsparły: %s." % funders

            isbn = getattr(meta, 'isbn_txt', None)
            if isbn:
                isbn = '\n\n' + isbn
            else:
                isbn = ''
                
            result = TEMPLATE % {
                "text": text,
                "description": meta.description,
                "url": meta.url,
                "license_description": license_description,
                "source": source,
                "contributors": contributors,
                "funders": funders,
                "publisher":  '\n\nWydawca: ' + ', '.join(meta.publisher),
                "isbn": isbn,
            }

        result = '\r\n'.join(result.splitlines()) + '\r\n'
        return OutputFile.from_bytes(result.encode('utf-8'))
