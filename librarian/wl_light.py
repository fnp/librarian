# -*- encoding: utf-8 -*-

__author__= "Łukasz Rekucki"
__date__ = "$2009-10-19 16:31:14$"
__doc__ = "Functions to operate on a tag-light version of WLML."

class LightSerializer(object):

    def __init__(self):
        pass

    def serialize(self, element):
        handler = getattr(self, 'serialize_' + element.tag, self.identity)
        return handler(element) + (element.tail or u'')

    def serialize_slowo_obce(self, e):
        return u' %%'+self.descent(e)+u'%% '

    def descent(self, e):
        b = (e.text or u'')
        for child in e.iterchildren():
            b += self.serialize(child)
        return b

    def identity(self, e):
        b = u'<'+e.tag
        
        # attributes
        b += u' '.join((u'%s="%s"' % (attr, value) for attr,value in e.items()))
        b += u'>'
        b += self.descent(e)       
        b += u'</' + e.tag + u'>'

        return b

_serializer = LightSerializer()

def serialize_nl(element):
    prolog = u'' + element.text # ordinary stuff
    data = u''

    for child in element.iterchildren():
        data += _serializer.serialize(child)

    return prolog + data
        

