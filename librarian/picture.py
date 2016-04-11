# -*- coding: utf-8 -*-
from operator import and_

from dcparser import Field, WorkInfo, DCNS
from librarian import (RDFNS, ValidationError, NoDublinCore, ParseError, WLURI)
from xml.parsers.expat import ExpatError
from os import path
from StringIO import StringIO
from lxml import etree
from lxml.etree import (XMLSyntaxError, XSLTApplyError, Element)
import re


class WLPictureURI(WLURI):
    _re_wl_uri = re.compile('http://wolnelektury.pl/katalog/obraz/(?P<slug>[-a-z0-9]+)/?$')

    @classmethod
    def from_slug(cls, slug):
        uri = 'http://wolnelektury.pl/katalog/obraz/%s/' % slug
        return cls(uri)


def as_wlpictureuri_strict(text):
    return WLPictureURI.strict(text)


class PictureInfo(WorkInfo):
    """
    Dublin core metadata for a picture
    """
    FIELDS = (
        Field(DCNS('language'), 'language', required=False),
        Field(DCNS('subject.period'), 'epochs', salias='epoch', multiple=True),
        Field(DCNS('subject.type'), 'kinds', salias='kind', multiple=True),
        Field(DCNS('subject.genre'), 'genres', salias='genre', multiple=True, required=False),
        Field(DCNS('subject.style'), 'styles', salias='style', multiple=True, required=False),

        Field(DCNS('format.dimensions'), 'dimensions', required=False),
        Field(DCNS('format.checksum.sha1'), 'sha1', required=True),
        Field(DCNS('description.medium'), 'medium', required=False),
        Field(DCNS('description.dimensions'), 'original_dimensions', required=False),
        Field(DCNS('format'), 'mime_type', required=False),
        Field(DCNS('identifier.url'), 'url', WLPictureURI, strict=as_wlpictureuri_strict)
    )


class ImageStore(object):
    EXT = ['gif', 'jpeg', 'png', 'swf', 'psd', 'bmp'
           'tiff', 'tiff', 'jpc', 'jp2', 'jpf', 'jb2', 'swc',
           'aiff', 'wbmp', 'xbm']
    MIME = ['image/gif', 'image/jpeg', 'image/png',
            'application/x-shockwave-flash', 'image/psd', 'image/bmp',
            'image/tiff', 'image/tiff', 'application/octet-stream',
            'image/jp2', 'application/octet-stream', 'application/octet-stream',
            'application/x-shockwave-flash', 'image/iff', 'image/vnd.wap.wbmp', 'image/xbm']

    def __init__(self, dir_):
        super(ImageStore, self).__init__()
        self.dir = dir_

    def path(self, slug, mime_type):
        """
        Finds file by slug and mime type in our iamge store.
        Returns a file objects (perhaps should return a filename?)
        """
        try:
            i = self.MIME.index(mime_type)
        except ValueError:
            err = ValueError("Picture %s has unknown mime type: %s" % (slug, mime_type))
            err.slug = slug
            err.mime_type = mime_type
            raise err
        ext = self.EXT[i]
        # add some common extensions tiff->tif, jpeg->jpg
        return path.join(self.dir, slug + '.' + ext)


class WLPicture(object):
    def __init__(self, edoc, parse_dublincore=True, image_store=None):
        self.edoc = edoc
        self.image_store = image_store

        root_elem = edoc.getroot()

        dc_path = './/' + RDFNS('RDF')

        if root_elem.tag != 'picture':
            raise ValidationError("Invalid root element. Found '%s', should be 'picture'" % root_elem.tag)

        if parse_dublincore:
            self.rdf_elem = root_elem.find(dc_path)

            if self.rdf_elem is None:
                raise NoDublinCore('Document has no DublinCore - which is required.')

            self.picture_info = PictureInfo.from_element(self.rdf_elem)
        else:
            self.picture_info = None
        self.frame = None

    @classmethod
    def from_string(cls, xml, *args, **kwargs):
        return cls.from_file(StringIO(xml), *args, **kwargs)

    @classmethod
    def from_file(cls, xmlfile, parse_dublincore=True, image_store=None):

        # first, prepare for parsing
        if isinstance(xmlfile, basestring):
            file = open(xmlfile, 'rb')
            try:
                data = file.read()
            finally:
                file.close()
        else:
            data = xmlfile.read()

        if not isinstance(data, unicode):
            data = data.decode('utf-8')

        data = data.replace(u'\ufeff', '')

        # assume images are in the same directory
        if image_store is None and getattr(xmlfile, 'name', None):
            image_store = ImageStore(path.dirname(xmlfile.name))

        try:
            parser = etree.XMLParser(remove_blank_text=False)
            tree = etree.parse(StringIO(data.encode('utf-8')), parser)

            me = cls(tree, parse_dublincore=parse_dublincore, image_store=image_store)
            me.load_frame_info()
            return me
        except (ExpatError, XMLSyntaxError, XSLTApplyError), e:
            raise ParseError(e)

    @property
    def mime_type(self):
        if self.picture_info is None:
            raise ValueError('DC is not loaded, hence we don\'t know the image type')
        return self.picture_info.mime_type

    @property
    def slug(self):
        return self.picture_info.url.slug

    @property
    def image_path(self):
        if self.image_store is None:
            raise ValueError("No image store associated with whis WLPicture.")

        return self.image_store.path(self.slug, self.mime_type)

    def image_file(self, *args, **kwargs):
        return open(self.image_path, *args, **kwargs)

    def get_sem_coords(self, sem):
        area = sem.find("div[@type='rect']")
        if area is None:
            area = sem.find("div[@type='whole']")
            return [[0, 0], [-1, -1]]

        def has_all_props(node, props):
            return reduce(and_, map(lambda prop: prop in node.attrib, props))

        if not has_all_props(area, ['x1', 'x2', 'y1', 'y2']):
            return None

        def n(prop): return int(area.get(prop))
        return [[n('x1'), n('y1')], [n('x2'), n('y2')]]

    def partiter(self):
        """
        Iterates the parts of this picture and returns them and their metadata
        """
        # omg no support for //sem[(@type='theme') or (@type='object')] ?
        for part in list(self.edoc.iterfind("//sem[@type='theme']")) +\
                list(self.edoc.iterfind("//sem[@type='object']")):
            pd = {'type': part.get('type')}

            coords = self.get_sem_coords(part)
            if coords is None:
                continue
            pd['coords'] = coords

            def want_unicode(x):
                if not isinstance(x, unicode):
                    return x.decode('utf-8')
                else:
                    return x
            pd['object'] = part.attrib['type'] == 'object' and want_unicode(part.attrib.get('object', u'')) or None
            pd['themes'] = part.attrib['type'] == 'theme' and [part.attrib.get('theme', u'')] or []
            yield pd

    def load_frame_info(self):
        k = self.edoc.find("//sem[@object='kadr']")
        
        if k is not None:
            clip = self.get_sem_coords(k)
            self.frame = clip
            frm = Element("sem", {"type": "frame"})
            frm.append(k.iter("div").next())
            self.edoc.getroot().append(frm)
            k.getparent().remove(k)
        else:
            frm = self.edoc.find("//sem[@type='frame']")
            if frm:
                self.frame = self.get_sem_coords(frm)
            else:
                self.frame = None
        return self
