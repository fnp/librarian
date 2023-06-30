# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
import os
from shutil import rmtree
from tempfile import mkdtemp
from fontTools.subset import main


def strip_font(path, chars):
    tmpdir = mkdtemp('-librarian-epub')
    main([
        path,
       '--text=' + ''.join(chars),
       '--output-file=' + os.path.join(tmpdir, 'font.ttf')
    ])
    with open(os.path.join(tmpdir, 'font.ttf'), 'rb') as f:
        content = f.read()

    rmtree(tmpdir)
    return content
