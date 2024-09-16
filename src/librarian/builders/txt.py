# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import io
from librarian import OutputFile, get_resource


with io.open(get_resource("res/text/template.txt")) as f:
    TEMPLATE = f.read()


class TxtFragment:
    def __init__(self):
        self.pieces = []
        self.current_margin = 0
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
    after_child_fn = 'txt_after_child'

    debug = False
    orphans = False
    normalize_whitespace = True
    
    default_license_description = {
        "pol": (
            "Wszystkie zasoby Wolnych Lektur możesz swobodnie wykorzystywać, "
            "publikować i rozpowszechniać pod warunkiem zachowania warunków "
            "licencji i zgodnie z Zasadami wykorzystania Wolnych Lektur.\n"
            "Ten utwór jest w domenie publicznej.\n"
            "Wszystkie materiały dodatkowe (przypisy, motywy literackie) są "
            "udostępnione na Licencji Wolnej Sztuki 1.3: "
            "https://artlibre.org/licence/lal/pl/\n"
            "Fundacja Wolne Lektury zastrzega sobie prawa do wydania "
            "krytycznego zgodnie z art. Art.99(2) Ustawy o prawach autorskich "
            "i prawach pokrewnych.\nWykorzystując zasoby z Wolnych Lektur, "
            "należy pamiętać o zapisach licencji oraz zasadach, które "
            "spisaliśmy w Zasadach wykorzystania Wolnych Lektur: "
            "https://wolnelektury.pl/info/zasady-wykorzystania/\nZapoznaj "
            "się z nimi, zanim udostępnisz dalej nasze książki."
        )
    }
    license_description = {
        "pol": (
            #"Ten utwór jest udostępniony na licencji {meta.license_description}: \n{meta.license}",
            "Wszystkie zasoby Wolnych Lektur możesz swobodnie wykorzystywać, "
            "publikować i rozpowszechniać pod warunkiem zachowania warunków "
            "licencji i zgodnie z Zasadami wykorzystania Wolnych Lektur.\n"
            "Ten utwór jest jest udostępniony na licencji {meta.license_description} ({meta.license}). "
            "Wszystkie materiały dodatkowe (przypisy, motywy literackie) są "
            "udostępnione na Licencji Wolnej Sztuki 1.3: "
            "https://artlibre.org/licence/lal/pl/\n"
            "Fundacja Wolne Lektury zastrzega sobie prawa do wydania "
            "krytycznego zgodnie z art. Art.99(2) Ustawy o prawach autorskich "
            "i prawach pokrewnych.\nWykorzystując zasoby z Wolnych Lektur, "
            "należy pamiętać o zapisach licencji oraz zasadach, które "
            "spisaliśmy w Zasadach wykorzystania Wolnych Lektur: "
            "https://wolnelektury.pl/info/zasady-wykorzystania/\nZapoznaj "
            "się z nimi, zanim udostępnisz dalej nasze książki."
        )
    }

    def __init__(self, base_url=None):
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
            builder.push_margin(2)

        if meta.isbn_txt:
            self.push_margin(2)
            isbn = meta.isbn_txt
            if isbn.startswith(('ISBN-' , 'ISBN ')):
                isbn = isbn[5:]
            self.push_text('ISBN {isbn}'.format(isbn=isbn))
            #builder.push_margin(5)

        self.push_margin(4)
        self.exit_fragment()
        
        text = ''.join(self.fragments[None].pieces).lstrip()

        if raw_text:
            result = text
        else:
            text = ''.join(self.fragments['header'].pieces) +  text

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
                funders = "\n\nPublikację wsparli i wsparły: %s." % funders

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
