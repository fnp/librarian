# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import os
import shutil
from subprocess import call, PIPE
from tempfile import mkdtemp
from librarian import get_resource
from . import DataEmbed, create_embed, downgrades_to


class LaTeX(DataEmbed):
    @downgrades_to('image/png')
    def to_png(self):
        with open(get_resource('res/embeds/latex/template.tex'), 'rb') as f:
            tmpl = f.read().decode('utf-8')
        tempdir = mkdtemp('-librarian-embed-latex')
        fpath = os.path.join(tempdir, 'doc.tex')
        with open(fpath, 'wb') as f:
            f.write((tmpl % {'code': self.data}).encode('utf-8'))
        call(['xelatex', '-interaction=batchmode', '-output-directory',
              tempdir, fpath], stdout=PIPE, stderr=PIPE)
        call(['convert', '-density', '150', os.path.join(tempdir, 'doc.pdf'),
              '-trim', os.path.join(tempdir, 'doc.png')])
        pngdata = open(os.path.join(tempdir, 'doc.png'), 'rb').read()
        shutil.rmtree(tempdir)
        return create_embed('image/png', data=pngdata)
