import re
from .base import MetaValue


class WLURI(MetaValue):
    """Represents a WL URI. Extracts slug from it."""
    template = 'http://wolnelektury.pl/katalog/lektura/%s/'
    _re_wl_uri = re.compile(
        r'http://(www\.)?wolnelektury.pl/katalog/lektur[ay]/'
        '(?P<slug>[-a-z0-9]+)/?$'
    )

    def __init__(self, slug, uri=None):
        """Contructs an URI from slug.

        >>> print(WLURI('a-slug').uri)
        http://wolnelektury.pl/katalog/lektura/a-slug/

        """
        if uri is None:
            uri = self.template % slug
        self.uri = uri
        return super().__init__(slug)

    @classmethod
    def from_text(cls, uri):
        slug = uri.rstrip('/').rsplit('/', 1)[-1]
        return cls(slug, uri)

    def validate(self):
        match = self._re_wl_uri.match(self.uri)
        if not match:
            raise ValidationError('Invalid URI (%s). Should match: %s' % (
                        self.uri, self._re_wl_uri.pattern))

    def __str__(self):
        return self.uri

    def __eq__(self, other):
        return self.value == other.value

    @property
    def slug(self):
        return self.value
