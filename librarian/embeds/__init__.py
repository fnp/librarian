import importlib
from lxml import etree

known_types = {
    'application/mathml+xml': 'librarian.embeds.mathml.MathML',
    'application/x-latex': 'librarian.embeds.latex.LaTeX',
}

class Embed():
    @classmethod
    def transforms_to(cls, mime_types, downgrade=False):
        matches = set()
        for name, method in cls.__dict__.iteritems():
            if hasattr(method, "embed_converts_to"):
                conv_type, conv_downgrade = method.embed_converts_to
                if downgrade == conv_downgrade and conv_type in mime_types:
                    matches.add(conv_type)
        return matches

    def transform_to(self, mime_type, downgrade=False):
        for name, method in type(cls).__dict__.iteritems():
            if hasattr(method, "embed_converts_to"):
                conv_type, conv_downgrade = method.embed_converts_to
                if downgrade == conv_downgrade and conv_type == mime_type:
                    return method(self)


class DataEmbed(Embed):
    def __init__(self, data=None):
        self.data = data

class TreeEmbed(Embed):
    def __init__(self, tree=None):
        if isinstance(tree, etree._Element):
            tree = etree.ElementTree(tree)
        self.tree = tree

def converts_to(mime_type, downgrade=False):
    def decorator(method):
        method.embed_converts_to = mime_type, downgrade
        return method
    return decorator

def downgrades_to(mime_type):
    return converts_to(mime_type, True)

def create_embed(mime_type, tree=None, data=None):
    embed = known_types.get(mime_type)
    if embed is None:
        embed = DataEmbed if tree is None else TreeEmbed
    else:
        mod_name, cls_name = embed.rsplit('.', 1)
        mod = importlib.import_module(mod_name)
        embed = getattr(mod, cls_name)

    return embed(data if tree is None else tree)
