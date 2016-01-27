# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from xml.parsers.expat import ExpatError
from datetime import date
import time
import re
from librarian.util import roman_to_int

from librarian import (ValidationError, NoDublinCore, ParseError, DCNS, RDFNS,
                       XMLNS, WLURI, WLNS, PLMETNS)

import lxml.etree as etree  # ElementTree API using libxml2
from lxml.etree import XMLSyntaxError


class TextPlus(unicode):
    pass


class DatePlus(date):
    pass


# ==============
# = Converters =
# ==============
class Person(object):
    """Single person with last name and a list of first names."""
    def __init__(self, last_name, *first_names):
        self.last_name = last_name
        self.first_names = first_names

    @classmethod
    def from_text(cls, text):
        parts = [token.strip() for token in text.split(',')]
        if len(parts) == 1:
            surname = parts[0]
            names = []
        elif len(parts) != 2:
            raise ValueError("Invalid person name. There should be at most one comma: \"%s\"." % text.encode('utf-8'))
        else:
            surname = parts[0]
            if len(parts[1]) == 0:
                # there is no non-whitespace data after the comma
                raise ValueError("Found a comma, but no names given: \"%s\" -> %r." % (text, parts))
            names = parts[1].split()
        return cls(surname, *names)

    def readable(self):
        return u" ".join(self.first_names + (self.last_name,))

    def __eq__(self, right):
        return self.last_name == right.last_name and self.first_names == right.first_names

    def __cmp__(self, other):
        return cmp((self.last_name, self.first_names), (other.last_name, other.first_names))

    def __hash__(self):
        return hash((self.last_name, self.first_names))

    def __unicode__(self):
        if len(self.first_names) > 0:
            return '%s, %s' % (self.last_name, ' '.join(self.first_names))
        else:
            return self.last_name

    def __repr__(self):
        return 'Person(last_name=%r, first_names=*%r)' % (self.last_name, self.first_names)


def as_date(text):
    """Dates for digitization of pictures. It seems we need the following:
ranges:		'1350-1450',
centuries:	"XVIII w.'
half centuries/decades: '2 poł. XVIII w.', 'XVII w., l. 20'
later-then: 'po 1450'
circa 'ok. 1813-1814', 'ok.1876-ok.1886
turn: 1893/1894
for now we will translate this to some single date losing information of course.
    """
    try:
        # check out the "N. poł X w." syntax
        if isinstance(text, str):
            text = text.decode("utf-8")

        century_format = u"(?:([12]) *poł[.]? +)?([MCDXVI]+) *w[.,]*(?: *l[.]? *([0-9]+))?"
        vague_format = u"(?:po *|ok. *)?([0-9]{4})(-[0-9]{2}-[0-9]{2})?"

        m = re.match(century_format, text)
        m2 = re.match(vague_format, text)
        if m:
            half = m.group(1)
            decade = m.group(3)
            century = roman_to_int(str(m.group(2)))
            if half is not None:
                if decade is not None:
                    raise ValueError("Bad date format. Cannot specify both half and decade of century")
                half = int(half)
                t = ((century*100 + (half-1)*50), 1, 1)
            else:
                decade = int(decade or 0)
                t = ((century*100 + decade), 1, 1)
        elif m2:
            year = m2.group(1)
            mon_day = m2.group(2)
            if mon_day:
                t = time.strptime(year + mon_day, "%Y-%m-%d")
            else:
                t = time.strptime(year, '%Y')
        else:
            raise ValueError

        return DatePlus(t[0], t[1], t[2])
    except ValueError, e:
        raise ValueError("Unrecognized date format. Try YYYY-MM-DD or YYYY.")


def as_person(text):
    return Person.from_text(text)


def as_unicode(text):
    if isinstance(text, unicode):
        return text
    else:
        return TextPlus(text.decode('utf-8'))


def as_wluri_strict(text):
    return WLURI.strict(text)


class Field(object):
    def __init__(self, uri, attr_name, validator=as_unicode, strict=None, multiple=False, salias=None, **kwargs):
        self.uri = uri
        self.name = attr_name
        self.validator = validator
        self.strict = strict
        self.multiple = multiple
        self.salias = salias

        self.required = kwargs.get('required', True) and 'default' not in kwargs
        self.default = kwargs.get('default', [] if multiple else [None])

    def validate_value(self, val, strict=False):
        if strict and self.strict is not None:
            validator = self.strict
        else:
            validator = self.validator
        try:
            if self.multiple:
                if validator is None:
                    return val
                new_values = []
                for v in val:
                    nv = v
                    if v is not None:
                        nv = validator(v)
                        if hasattr(v, 'lang'):
                            setattr(nv, 'lang', v.lang)
                    new_values.append(nv)
                return new_values
            elif len(val) > 1:
                raise ValidationError("Multiple values not allowed for field '%s'" % self.uri)
            elif len(val) == 0:
                raise ValidationError("Field %s has no value to assign. Check your defaults." % self.uri)
            else:
                if validator is None or val[0] is None:
                    return val[0]
                nv = validator(val[0])
                if hasattr(val[0], 'lang'):
                    setattr(nv, 'lang', val[0].lang)
                return nv
        except ValueError, e:
            raise ValidationError("Field '%s' - invald value: %s" % (self.uri, e.message))

    def validate(self, fdict, fallbacks=None, strict=False):
        if fallbacks is None:
            fallbacks = {}
        if self.uri not in fdict:
            if not self.required:
                # Accept single value for single fields and saliases.
                if self.name in fallbacks:
                    if self.multiple:
                        f = fallbacks[self.name]
                    else:
                        f = [fallbacks[self.name]]
                elif self.salias and self.salias in fallbacks:
                    f = [fallbacks[self.salias]]
                else:
                    f = self.default
            else:
                raise ValidationError("Required field %s not found" % self.uri)
        else:
            f = fdict[self.uri]

        return self.validate_value(f, strict=strict)

    def __eq__(self, other):
        if isinstance(other, Field) and other.name == self.name:
            return True
        return False


class DCInfo(type):
    def __new__(mcs, classname, bases, class_dict):
        fields = list(class_dict['FIELDS'])

        for base in bases[::-1]:
            if hasattr(base, 'FIELDS'):
                for field in base.FIELDS[::-1]:
                    try:
                        fields.index(field)
                    except ValueError:
                        fields.insert(0, field)

        class_dict['FIELDS'] = tuple(fields)
        return super(DCInfo, mcs).__new__(mcs, classname, bases, class_dict)


class WorkInfo(object):
    __metaclass__ = DCInfo

    FIELDS = (
        Field(DCNS('creator'), 'authors', as_person, salias='author', multiple=True),
        Field(DCNS('title'), 'title'),
        Field(DCNS('type'), 'type', required=False, multiple=True),

        Field(DCNS('contributor.editor'), 'editors',
              as_person, salias='editor', multiple=True, default=[]),
        Field(DCNS('contributor.technical_editor'), 'technical_editors',
              as_person, salias='technical_editor', multiple=True, default=[]),
        Field(DCNS('contributor.funding'), 'funders', salias='funder', multiple=True, default=[]),
        Field(DCNS('contributor.thanks'), 'thanks', required=False),

        Field(DCNS('date'), 'created_at'),
        Field(DCNS('date.pd'), 'released_to_public_domain_at', as_date, required=False),
        Field(DCNS('publisher'), 'publisher'),

        Field(DCNS('language'), 'language'),
        Field(DCNS('description'), 'description', required=False),

        Field(DCNS('source'), 'source_name', required=False),
        Field(DCNS('source.URL'), 'source_url', required=False),
        Field(DCNS('identifier.url'), 'url', WLURI, strict=as_wluri_strict),
        Field(DCNS('rights.license'), 'license', required=False),
        Field(DCNS('rights'), 'license_description'),

        Field(PLMETNS('digitisationSponsor'), 'sponsors', multiple=True, default=[]),
        Field(WLNS('digitisationSponsorNote'), 'sponsor_note', required=False),
        Field(WLNS('developmentStage'), 'stage', required=False),
    )

    @classmethod
    def from_string(cls, xml, *args, **kwargs):
        from StringIO import StringIO
        return cls.from_file(StringIO(xml), *args, **kwargs)

    @classmethod
    def from_file(cls, xmlfile, *args, **kwargs):
        desc_tag = None
        try:
            iter = etree.iterparse(xmlfile, ['start', 'end'])
            for (event, element) in iter:
                if element.tag == RDFNS('RDF') and event == 'start':
                    desc_tag = element
                    break

            if desc_tag is None:
                raise NoDublinCore("DublinCore section not found. \
                    Check if there are rdf:RDF and rdf:Description tags.")

            # continue 'till the end of RDF section
            for (event, element) in iter:
                if element.tag == RDFNS('RDF') and event == 'end':
                    break

            # if there is no end, Expat should yell at us with an ExpatError

            # extract data from the element and make the info
            return cls.from_element(desc_tag, *args, **kwargs)
        except XMLSyntaxError, e:
            raise ParseError(e)
        except ExpatError, e:
            raise ParseError(e)

    @classmethod
    def from_element(cls, rdf_tag, *args, **kwargs):
        # the tree is already parsed, so we don't need to worry about Expat errors
        field_dict = {}
        desc = rdf_tag.find(".//" + RDFNS('Description'))

        if desc is None:
            raise NoDublinCore("No DublinCore section found.")

        lang = None
        p = desc
        while p is not None and lang is None:
            lang = p.attrib.get(XMLNS('lang'))
            p = p.getparent()

        for e in desc.getchildren():
            fv = field_dict.get(e.tag, [])
            if e.text is not None:
                text = e.text
                if not isinstance(text, unicode):
                    text = text.decode('utf-8')
                val = TextPlus(text)
                val.lang = e.attrib.get(XMLNS('lang'), lang)
            else:
                val = e.text
            fv.append(val)
            field_dict[e.tag] = fv

        return cls(desc.attrib, field_dict, *args, **kwargs)

    def __init__(self, rdf_attrs, dc_fields, fallbacks=None, strict=False):
        """rdf_attrs should be a dictionary-like object with any attributes of the RDF:Description.
        dc_fields - dictionary mapping DC fields (with namespace) to list of text values for the
        given field. """

        self.about = rdf_attrs.get(RDFNS('about'))
        self.fmap = {}

        for field in self.FIELDS:
            value = field.validate(dc_fields, fallbacks=fallbacks, strict=strict)
            setattr(self, 'prop_' + field.name, value)
            self.fmap[field.name] = field
            if field.salias:
                self.fmap[field.salias] = field

    def __getattribute__(self, name):
        try:
            field = object.__getattribute__(self, 'fmap')[name]
            value = object.__getattribute__(self, 'prop_'+field.name)
            if field.name == name:
                return value
            else:  # singular alias
                if not field.multiple:
                    raise "OUCH!! for field %s" % name

                return value[0] if value else None
        except (KeyError, AttributeError):
            return object.__getattribute__(self, name)

    def __setattr__(self, name, newvalue):
        try:
            field = object.__getattribute__(self, 'fmap')[name]
            if field.name == name:
                object.__setattr__(self, 'prop_'+field.name, newvalue)
            else:  # singular alias
                if not field.multiple:
                    raise "OUCH! while setting field %s" % name

                object.__setattr__(self, 'prop_'+field.name, [newvalue])
        except (KeyError, AttributeError):
            return object.__setattr__(self, name, newvalue)

    def update(self, field_dict):
        """Update using field_dict. Verify correctness, but don't check if all
        required fields are present."""
        for field in self.FIELDS:
            if field.name in field_dict:
                setattr(self, field.name, field_dict[field.name])

    def to_etree(self, parent=None):
        """XML representation of this object."""
        # etree._namespace_map[str(self.RDF)] = 'rdf'
        # etree._namespace_map[str(self.DC)] = 'dc'

        if parent is None:
            root = etree.Element(RDFNS('RDF'))
        else:
            root = parent.makeelement(RDFNS('RDF'))

        description = etree.SubElement(root, RDFNS('Description'))

        if self.about:
            description.set(RDFNS('about'), self.about)

        for field in self.FIELDS:
            v = getattr(self, field.name, None)
            if v is not None:
                if field.multiple:
                    if len(v) == 0:
                        continue
                    for x in v:
                        e = etree.Element(field.uri)
                        if x is not None:
                            e.text = unicode(x)
                        description.append(e)
                else:
                    e = etree.Element(field.uri)
                    e.text = unicode(v)
                    description.append(e)

        return root

    def serialize(self):
        rdf = {'about': {'uri': RDFNS('about'), 'value': self.about}}

        dc = {}
        for field in self.FIELDS:
            v = getattr(self, field.name, None)
            if v is not None:
                if field.multiple:
                    if len(v) == 0:
                        continue
                    v = [unicode(x) for x in v if x is not None]
                else:
                    v = unicode(v)

                dc[field.name] = {'uri': field.uri, 'value': v}
        rdf['fields'] = dc
        return rdf

    def to_dict(self):
        result = {'about': self.about}
        for field in self.FIELDS:
            v = getattr(self, field.name, None)

            if v is not None:
                if field.multiple:
                    if len(v) == 0:
                        continue
                    v = [unicode(x) for x in v if x is not None]
                else:
                    v = unicode(v)
                result[field.name] = v

            if field.salias:
                v = getattr(self, field.salias)
                if v is not None:
                    result[field.salias] = unicode(v)

        return result


class BookInfo(WorkInfo):
    FIELDS = (
        Field(DCNS('audience'), 'audiences', salias='audience', multiple=True, required=False),

        Field(DCNS('subject.period'), 'epochs', salias='epoch', multiple=True, required=False),
        Field(DCNS('subject.type'), 'kinds', salias='kind', multiple=True, required=False),
        Field(DCNS('subject.genre'), 'genres', salias='genre', multiple=True, required=False),
                
        Field(DCNS('contributor.translator'), 'translators',
              as_person,  salias='translator', multiple=True, default=[]),
        Field(DCNS('relation.hasPart'), 'parts', WLURI, strict=as_wluri_strict, multiple=True, required=False),
        Field(DCNS('relation.isVariantOf'), 'variant_of', WLURI, strict=as_wluri_strict, required=False),

        Field(DCNS('relation.coverImage.url'), 'cover_url', required=False),
        Field(DCNS('relation.coverImage.attribution'), 'cover_by', required=False),
        Field(DCNS('relation.coverImage.source'), 'cover_source', required=False),
        # WLCover-specific.
        Field(WLNS('coverBarColor'), 'cover_bar_color', required=False),
        Field(WLNS('coverBoxPosition'), 'cover_box_position', required=False),
    )


def parse(file_name, cls=BookInfo):
    return cls.from_file(file_name)
