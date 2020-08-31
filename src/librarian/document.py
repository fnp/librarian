from lxml import etree
from .builders import get_builder_class
from .parser import parser
from . import dcparser


class WLDocument:
    def __init__(self, tree=None, filename=None):
        if filename is not None:
            tree = etree.parse(filename, parser=parser)
        self.tree = tree
        tree.getroot().document = self
        self.base_meta = dcparser.BookInfo({}, {}, validate_required=False)

    @property
    def meta(self):
        # Allow metadata of the master element as document meta.
        #master = self.tree.getroot()[-1]
        return self.tree.getroot().meta
        return master.meta

    def build(self, builder_id, **kwargs):
        return get_builder_class(builder_id)().build(self, **kwargs)
        
