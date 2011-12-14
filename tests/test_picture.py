# -*- coding: utf-8 -*-
#
# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from librarian import picture, dcparser
from lxml import etree
from nose.tools import *
from os.path import splitext
from tests.utils import get_all_fixtures, get_fixture
import codecs
from os import path

def test_wlpictureuri():
    uri = picture.WLPictureURI('http://wolnelektury.pl/katalog/obraz/angelus-novus')

def check_load(xml_file):
    pi = dcparser.parse(xml_file, picture.PictureInfo)
    assert pi is not None
    assert isinstance(pi, picture.PictureInfo)
    

def test_load():
    for fixture in get_all_fixtures('picture', '*.xml'):
        yield check_load, fixture


def test_wlpicture():
    wlp = picture.WLPicture.from_file(open(get_fixture('picture', 'angelus-novus.xml')))
    pi = wlp.picture_info

    #    from nose.tools import set_trace; set_trace()
    assert pi.type[0] == u"Image"
    assert pi.mime_type == u'image/png' == wlp.mime_type
    assert wlp.slug == 'angelus-novus'

    assert path.exists(wlp.image_path)
    
    f = wlp.image_file('r')
    f.close()
