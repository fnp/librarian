# -*- coding: utf-8 -*-
from xml.parsers.expat import ExpatError
from datetime import date
import time

# Import ElementTree from anywhere
try:
    import xml.etree.ElementTree as etree # Python >= 2.5
except ImportError:
    try:
        import elementtree.ElementTree as etree # effbot's pure Python module
    except ImportError:
        import lxml.etree as etree # ElementTree API using libxml2


# ==============
# = Converters =
# ==============
class Person(object):
    """Single person with last name and a list of first names."""
    def __init__(self, last_name, *first_names):
        self.last_name = last_name
        self.first_names = first_names
    
    
    def __eq__(self, right):
        return self.last_name == right.last_name and self.first_names == right.first_names
    
    
    def __unicode__(self):
        if len(self.first_names) > 0:
            return '%s, %s' % (self.last_name, ' '.join(self.first_names))
        else:
            return self.last_name
    
    
    def __repr__(self):
        return 'Person(last_name=%r, first_names=*%r)' % (self.last_name, self.first_names)


def str_to_unicode(value, previous):
    return unicode(value)


def str_to_unicode_list(value, previous):
    if previous is None:
        previous = []
    previous.append(str_to_unicode(value, None))
    return previous


def str_to_person(value, previous):
    comma_count = value.count(',')
    
    if comma_count == 0:
        last_name, first_names = value, []
    elif comma_count == 1:
        last_name, first_names = value.split(',')
        first_names = [name for name in first_names.split(' ') if len(name)]
    else:
        raise ValueError("value contains more than one comma: %r" % value)
    
    return Person(last_name.strip(), *first_names)


def str_to_date(value, previous):
    try:
        t = time.strptime(value, '%Y-%m-%d')
    except ValueError:
        t = time.strptime(value, '%Y')
    return date(t[0], t[1], t[2])


# ==========
# = Parser =
# ==========
class ParseError(Exception):
    def __init__(self, message):
        super(ParseError, self).__init__(message)


class XMLNamespace(object):
    '''Represents XML namespace.'''
    
    def __init__(self, uri):
        self.uri = uri

    def __call__(self, tag):
        return '{%s}%s' % (self.uri, tag)

    def __contains__(self, tag):
        return tag.startswith(str(self))

    def __repr__(self):
        return 'XMLNamespace(%r)' % self.uri
    
    def __str__(self):
        return '%s' % self.uri


class BookInfo(object):
    RDF = XMLNamespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
    DC = XMLNamespace('http://purl.org/dc/elements/1.1/')
    
    mapping = {
        DC('creator')        : ('author', str_to_person),
        DC('title')          : ('title', str_to_unicode),
        DC('subject.period') : ('epoch', str_to_unicode),
        DC('subject.type')   : ('kind', str_to_unicode),
        DC('subject.genre')  : ('genre', str_to_unicode),
        DC('date')           : ('created_at', str_to_date),
        DC('date.pd')        : ('released_to_public_domain_at', str_to_date),
        DC('contributor.translator') : ('translator', str_to_person),
        DC('contributor.technical_editor') : ('technical_editor', str_to_person),
        DC('publisher')      : ('publisher', str_to_unicode),
        DC('source')         : ('source_name', str_to_unicode),
        DC('source.URL')     : ('source_url', str_to_unicode),
        DC('identifier.url') : ('url', str_to_unicode),
        DC('relation.hasPart') : ('parts', str_to_unicode_list),
        DC('rights.license') : ('license', str_to_unicode),
        DC('rights')         : ('license_description', str_to_unicode), 
    }

    @classmethod
    def from_string(cls, xml):
        from StringIO import StringIO
        return cls.from_file(StringIO(xml))
    
    @classmethod
    def from_file(cls, xml_file):
        book_info = cls()
        
        try:
            tree = etree.parse(xml_file)
        except ExpatError, e:
            raise ParseError(e)

        description = tree.find('//' + book_info.RDF('Description'))
        book_info.wiki_url = description.get(cls.RDF('about'), None)
        
        if description is None:
            raise ParseError('no Description tag found in document')
        
        for element in description.findall('*'):
            book_info.parse_element(element) 
        
        return book_info

    def parse_element(self, element):
        try:
            attribute, converter = self.mapping[element.tag]
            setattr(self, attribute, converter(element.text, getattr(self, attribute, None)))
        except KeyError:
            pass

    def to_xml(self):
        """XML representation of this object."""
        etree._namespace_map[str(self.RDF)] = 'rdf'
        etree._namespace_map[str(self.DC)] = 'dc'
        
        root = etree.Element(self.RDF('RDF'))
        description = etree.SubElement(root, self.RDF('Description'))
        
        if self.wiki_url:
            description.set(self.RDF('about'), self.wiki_url)
        
        for tag, (attribute, converter) in self.mapping.iteritems():
            if hasattr(self, attribute):
                e = etree.Element(tag)
                e.text = unicode(getattr(self, attribute))
                description.append(e)
        
        return unicode(etree.tostring(root, 'utf-8'), 'utf-8')

    def to_dict(self):
        etree._namespace_map[str(self.RDF)] = 'rdf'
        etree._namespace_map[str(self.DC)] = 'dc'
        
        result = {'about': self.wiki_url}
        for tag, (attribute, converter) in self.mapping.iteritems():
            if hasattr(self, attribute):
                result[attribute] = unicode(getattr(self, attribute))
        
        return result


def parse(file_name):
    return BookInfo.from_file(file_name)


if __name__ == '__main__':
    import sys
    
    info = parse(sys.argv[1])
    for attribute, _ in BookInfo.mapping.values():
        print '%s: %r' % (attribute, getattr(info, attribute, None))

