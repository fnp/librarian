from lxml import etree
from librarian import OutputFile


class HtmlBuilder:
    file_extension = "html"
    identifier = "html"

    def __init__(self, image_location='https://wolnelektury.pl/media/book/pictures/marcos-historia-kolorow/'):
        self.image_location = image_location

        #self.tree = etree.Element('html')
        #body = etree.SubElement(self.tree, 'body')
        #text = etree.SubElement(body, 'div', **{'id': 'book-text'})
        self.tree = text = etree.Element('div', **{'id': 'book-text'})
        toc = etree.SubElement(text, 'div', id='toc')
        themes = etree.SubElement(text, 'div', id='themes')
        h1 = etree.SubElement(text, 'h1')

        self.cursors = {
            None: text,
            'toc': toc,
            'themes': themes,
            'header': h1,
        }
        self.current_cursors = [None]

    def enter_fragment(self, fragment):
        self.current_cursors.append(fragment)

    def exit_fragment(self):
        self.current_cursors.pop()
        
    def build(self, document):
        document.tree.getroot().html_build(self)

        head = etree.Element('head')
        self.tree.insert(0, head)
        etree.SubElement(
            head,
            'link',
            href="https://static.wolnelektury.pl/css/compressed/book_text.b15153e56c0a.css",
            rel="stylesheet",
            type="text/css",
        )
        
        return OutputFile.from_bytes(
            etree.tostring(
                self.tree,
                method='html',
                encoding='utf-8',
                pretty_print=True
            )
        )

    def start_element(self, tag, attrib):
        self.cursors[self.current_cursors[-1]] = etree.SubElement(
            self.cursors[self.current_cursors[-1]],
            tag,
            **attrib
        )
        print(self.cursors)

    def end_element(self):
        self.cursors[self.current_cursors[-1]] = self.cursors[self.current_cursors[-1]].getparent()

    def push_text(self, text):
        cursor = self.cursors[self.current_cursors[-1]]
        if len(cursor):
            cursor.tail = (cursor[-1].tail or '') + text
        else:
            cursor.text = (cursor.text or '') + text
