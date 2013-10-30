# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#

from nose.tools import *
from librarian.latex import LatexFragment
import os

def test_latex_to_png():
    lf = LatexFragment("$ \sum_{i = 0}^{123} n_i^{3}$")
    name1 = lf.filename
    assert_equal(name1.find("/"), -1)
    name = lf.path
    assert_true(os.path.exists(name))
    print os.stat(name)
    assert_true(os.stat(name).st_size > 0)
    lf.remove()
