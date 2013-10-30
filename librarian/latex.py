# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#

from os import path, system, popen2, unlink, rename
from tempfile import NamedTemporaryFile
import sys

class LatexFragment(object):
    def __init__(self, code, image_format='png', dirname="/tmp", resize=None):
        self.code = code
        self.temp = None
        self.format = image_format
        self.dirname = dirname
        self.resize = resize
        
    def generate(self):
        if self.temp is not None: 
            return
        self.temp = NamedTemporaryFile('r', 
                                  suffix='.'+self.format, 
                                  prefix=path.join(self.dirname,'librarian-latex-'),
                                  delete=False)
        try:
            (processor, _out) = popen2("l2p -o '%(out)s' -d 1200" 
                                     % {'out': self.temp.name},
                                     "w")
            
            processor.write(isinstance(self.code, unicode) and \
                            self.code.encode('utf-8') or\
                            self.code)
            print "LATEX: %s" % isinstance(self.code, unicode) and \
                            self.code.encode('utf-8') or\
                            self.code
            processor.close()
            _out.read() # waits for the process to finish

            # Resize the image if needed
            if self.resize:
                n, e =  path.splitext(self.path)
                aside_name = n + "_orig" + e
                rename(self.path, aside_name)
                system("convert -resize x%d %s %s" % (self.resize, aside_name, self.path))

        except Exception as e:
            import pdb; pdb.set_trace()
            if path.exists(self.temp.name):
                unlink(self.temp.name)
            raise e

    @property
    def filename(self, splitext=False):
        self.generate()
        n = path.basename(self.temp.name)
        if splitext: 
            return path.splitext(n)
        return n

    @property
    def path(self):
        return path.join(self.dirname, self.filename)

    def remove(self):
        if self.temp:
            unlink(self.temp.name)
            self.temp = None

    __del__ = remove
