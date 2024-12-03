# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from xml.parsers.expat import ExpatError
from datetime import date
import io
import time
import re
from librarian.util import roman_to_int

from librarian import (ValidationError, NoDublinCore, ParseError, DCNS, RDFNS,
                       XMLNS, WLNS, PLMETNS)

import lxml.etree as etree
from lxml.etree import XMLSyntaxError

from librarian.meta.types.bool import BoolValue
from librarian.meta.types.person import Person
from librarian.meta.types.wluri import WLURI
from librarian.meta.types import text


class Field:
    def __init__(self, uri, attr_name, value_type=text.TextValue,
                 multiple=False, salias=None, **kwargs):
        self.uri = uri
        self.name = attr_name
        self.value_type = value_type
        self.multiple = multiple
        self.salias = salias

        self.required = (kwargs.get('required', True)
                         and 'default' not in kwargs)
        self.default = kwargs.get('default', [] if multiple else [None])

    def validate_value(self, val, strict=False):
        #if strict:
        #    value.validate()

        try:
            if self.multiple:
                return val
            elif len(val) > 1:
                raise ValidationError(
                    "Multiple values not allowed for field '%s'" % self.uri
                )
            elif len(val) == 0:
                raise ValidationError(
                    "Field %s has no value to assign. Check your defaults."
                    % self.uri
                )
            else:
                return val[0]
        except ValueError as e:
            raise ValidationError(
                "Field '%s' - invald value: %s"
                % (self.uri, str(e))
            )

    def validate(self, fdict, fallbacks=None, strict=False, validate_required=True):
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
            elif validate_required:
                raise ValidationError("Required field %s not found" % self.uri)
            else:
                return None
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


class WorkInfo(metaclass=DCInfo):
    FIELDS = (
        Field(DCNS('creator'), 'authors', Person, salias='author',
              multiple=True, required=False),
        Field(DCNS('title'), 'title'),
        Field(DCNS('type'), 'type', required=False, multiple=True),

        Field(DCNS('contributor.editor'), 'editors',
              Person, salias='editor', multiple=True, required=False),
        Field(DCNS('contributor.technical_editor'), 'technical_editors',
              Person, salias='technical_editor', multiple=True,
              required=False),
        Field(DCNS('contributor.funding'), 'funders', salias='funder',
              multiple=True, required=False),
        Field(DCNS('contributor.thanks'), 'thanks', required=False),

        Field(DCNS('date'), 'created_at'),
        Field(DCNS('date.pd'), 'released_to_public_domain_at',
              required=False),
        Field(DCNS('publisher'), 'publisher', multiple=True),

        Field(DCNS('language'), 'language'),
        Field(DCNS('description'), 'description', required=False),

        Field(DCNS('source'), 'source_name', required=False),
        Field(DCNS('source.URL'), 'source_urls', salias='source_url',
              multiple=True, required=False),
        Field(DCNS('identifier.url'), 'url', WLURI),
        Field(DCNS('rights.license'), 'license', required=False),
        Field(DCNS('rights'), 'license_description'),

        Field(PLMETNS('digitisationSponsor'), 'sponsors', multiple=True,
              required=False),
        Field(WLNS('digitisationSponsorNote'), 'sponsor_note', required=False),
        Field(WLNS('contentWarning'), 'content_warnings', multiple=True,
              required=False),
        Field(WLNS('developmentStage'), 'stage', required=False),
        Field(WLNS('original'), 'original', required=False),
    )

    @classmethod
    def get_field_by_uri(cls, uri):
        for f in cls.FIELDS:
            if f.uri == uri:
                return f
    
    @classmethod
    def from_bytes(cls, xml, *args, **kwargs):
        return cls.from_file(io.BytesIO(xml), *args, **kwargs)

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
        except XMLSyntaxError as e:
            raise ParseError(e)
        except ExpatError as e:
            raise ParseError(e)

    @classmethod
    def from_element(cls, rdf_tag, *args, **kwargs):
        # The tree is already parsed,
        # so we don't need to worry about Expat errors.
        field_dict = {}
        desc = rdf_tag.find(".//" + RDFNS('Description'))

        if desc is None:
            raise NoDublinCore(
                "There must be a '%s' element inside the RDF."
                % RDFNS('Description')
            )

        lang = None
        p = desc
        while p is not None and lang is None:
            lang = p.attrib.get(XMLNS('lang'))
            p = p.getparent()

        for e in desc.getchildren():
            tag = e.tag
            if tag == 'meta':
                meta_id = e.attrib.get('id')
                if meta_id and meta_id.endswith('-id'):
                    tag = meta_id

            field = cls.get_field_by_uri(tag)
            if field is None:
                # Ignore unknown fields.
                continue

            fv = field_dict.get(tag, [])
            if e.text is not None:
                val = field.value_type.from_text(e.text)
                val.lang = e.attrib.get(XMLNS('lang'), lang)
            else:
                val = e.text
            fv.append(val)
            field_dict[tag] = fv

        return cls(desc.attrib, field_dict, *args, **kwargs)

    def __init__(self, rdf_attrs, dc_fields, fallbacks=None, strict=False, validate_required=True):
        """
        rdf_attrs should be a dictionary-like object with any attributes
        of the RDF:Description.
        dc_fields - dictionary mapping DC fields (with namespace) to
        list of text values for the given field.
        """

        self.about = rdf_attrs.get(RDFNS('about'))
        self.fmap = {}

        for field in self.FIELDS:
            value = field.validate(dc_fields, fallbacks=fallbacks,
                                   strict=strict, validate_required=validate_required)
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
        """
        Update using field_dict. Verify correctness, but don't check
        if all required fields are present.
        """
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
                            e.text = str(x)
                        description.append(e)
                else:
                    e = etree.Element(field.uri)
                    e.text = str(v)
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
                    v = [str(x) for x in v if x is not None]
                else:
                    v = str(v)

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
                    v = [str(x) for x in v if x is not None]
                else:
                    v = str(v)
                result[field.name] = v

            if field.salias:
                v = getattr(self, field.salias)
                if v is not None:
                    result[field.salias] = str(v)

        return result


class BookInfo(WorkInfo):
    FIELDS = (
        Field(DCNS('audience'), 'audiences', text.Audience, salias='audience', multiple=True,
              required=False),

        Field(DCNS('subject.period'), 'epochs', text.Epoch, salias='epoch', multiple=True,
              required=False),
        Field(DCNS('subject.type'), 'kinds', text.Kind, salias='kind', multiple=True,
              required=False),
        Field(DCNS('subject.genre'), 'genres', text.Genre, salias='genre', multiple=True,
              required=False),
        Field('category.legimi', 'legimi', text.LegimiCategory, required=False),
        Field('category.thema.main', 'thema_main', text.MainThemaCategory, required=False),
        Field('category.thema', 'thema', text.ThemaCategory, required=False, multiple=True),
        Field(DCNS('subject.location'), 'location', required=False),

        Field(DCNS('contributor.translator'), 'translators',
              Person,  salias='translator', multiple=True, required=False),
        Field(DCNS('relation.hasPart'), 'parts', WLURI,
              multiple=True, required=False),
        Field(DCNS('relation.isVariantOf'), 'variant_of', WLURI,
              required=False),

        Field(DCNS('relation.coverImage.url'), 'cover_url', required=False),
        Field(DCNS('relation.coverImage.attribution'), 'cover_by',
              required=False),
        Field(DCNS('relation.coverImage.source'), 'cover_source',
              required=False),
        # WLCover-specific.
        Field(WLNS('coverBarColor'), 'cover_bar_color', required=False),
        Field(WLNS('coverBoxPosition'), 'cover_box_position', required=False),
        Field(WLNS('coverClass'), 'cover_class', default=['default']),
        Field(WLNS('coverLogoUrl'), 'cover_logo_urls', multiple=True,
              required=False),
        Field(WLNS('endnotes'), 'endnotes', BoolValue,
              required=False),

        Field('pdf-id',  'isbn_pdf',  required=False),
        Field('epub-id', 'isbn_epub', required=False),
        Field('mobi-id', 'isbn_mobi', required=False),
        Field('txt-id',  'isbn_txt',  required=False),
        Field('html-id', 'isbn_html', required=False),
    )


def parse(file_name, cls=BookInfo):
    return cls.from_file(file_name)
