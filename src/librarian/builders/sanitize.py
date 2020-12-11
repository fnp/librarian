from lxml import etree
from librarian import OutputFile


class Sanitizer:
    identifier = 'sanitize'
    file_extension = 'xml2'

    def build(self, document, **kwargs):
        doc = document.tree.getroot() # TODO: copy
        doc.sanitize()
        return OutputFile.from_bytes(
            etree.tostring(
                doc,
                encoding='utf-8',
            )
        )

