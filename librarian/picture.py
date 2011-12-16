
from dcparser import (as_person, as_date, Field, WorkInfo, DCNS)
from librarian import (RDFNS, ValidationError, NoDublinCore, ParseError, WLURI)
from xml.parsers.expat import ExpatError
from os import path
from StringIO import StringIO
from lxml import etree
from lxml.etree import (XMLSyntaxError, XSLTApplyError)
import re


class WLPictureURI(WLURI):
    _re_wl_uri = re.compile('http://wolnelektury.pl/katalog/obraz/'
            '(?P<slug>[-a-z0-9]+)(/(?P<lang>[a-z]{3}))?/?$')

    def __init__(self, *args, **kw):
        super(WLPictureURI, self).__init__(*args, **kw)

    @classmethod
    def from_slug_and_lang(cls, slug, lang):
        uri = 'http://wolnelektury.pl/katalog/obraz/%s/' % slug
        return cls(uri)

    def filename_stem(self):
        return self.slug


class PictureInfo(WorkInfo):
    """
    Dublin core metadata for a picture
    """
    FIELDS = (
        Field(DCNS('format.dimensions.digital'), 'dimensions', required=False),
        Field(DCNS('format.dimensions.original'), 'dimensions_original', required=False),
        Field(DCNS('format.physical'), 'physical', required=False),
        Field(DCNS('format'), 'mime_type', required=False),
        Field(DCNS('identifier.url'), 'url', WLPictureURI),
        )

    def validate(self):
        """
        WorkInfo has a language validation code only, which we do not need.
        """
        pass
    

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
        self.dir = dir_
        return super(ImageStore, self).__init__()

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
        if image_store is None and xmlfile.name is not None:
            image_store = ImageStore(path.dirname(xmlfile.name))

        try:
            parser = etree.XMLParser(remove_blank_text=False)
            tree = etree.parse(StringIO(data.encode('utf-8')), parser)

            return cls(tree, parse_dublincore=parse_dublincore, image_store=image_store)
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
