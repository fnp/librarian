# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os
import shutil


class OutputFile(object):
    """Represents a file returned by one of the converters."""

    _string = None
    _filename = None

    def __del__(self):
        if self._filename:
            os.unlink(self._filename)

    def __nonzero__(self):
        return self._string is not None or self._filename is not None

    @classmethod
    def from_string(cls, string):
        """Converter returns contents of a file as a string."""

        instance = cls()
        instance._string = string
        return instance

    @classmethod
    def from_filename(cls, filename):
        """Converter returns contents of a file as a named file."""

        instance = cls()
        instance._filename = filename
        return instance

    def get_string(self):
        """Get file's contents as a string."""

        if self._filename is not None:
            with open(self._filename) as f:
                return f.read()
        else:
            return self._string

    def get_file(self):
        """Get file as a file-like object."""

        if self._string is not None:
            from StringIO import StringIO
            return StringIO(self._string)
        elif self._filename is not None:
            return open(self._filename)

    def get_filename(self):
        """Get file as a fs path."""

        if self._filename is not None:
            return self._filename
        elif self._string is not None:
            from tempfile import NamedTemporaryFile
            temp = NamedTemporaryFile(prefix='librarian-', delete=False)
            temp.write(self._string)
            temp.close()
            self._filename = temp.name
            return self._filename
        else:
            return None

    def save_as(self, path):
        """Save file to a path. Create directories, if necessary."""

        dirname = os.path.dirname(os.path.abspath(path))
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        shutil.copy(self.get_filename(), path)
