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
    assert pi.mime_type == u'image/jpeg' == wlp.mime_type
    assert wlp.slug == 'angelus-novus'

    assert path.exists(wlp.image_path)
    
    f = wlp.image_file('r')
    f.close()

def test_picture_parts():
    wlp = picture.WLPicture.from_file(open(get_fixture('picture', 'angelus-novus.xml')))
    parts = list(wlp.partiter())
    assert len(parts) == 5, "there should be %d parts of the picture" % 5
    motifs = set()
    names = set()

    print parts
    for p in parts:
        for m in p['themes']:
            motifs.add(m)
    for p in parts:
        if p['object']:
            names.add(p['object'])

    assert motifs == set([u'anioł historii', u'spojrzenie']), "missing motifs, got: %s" % motifs
    assert names == set([u'obraz cały', u'skrzydło']), 'missing objects, got: %s' % names
    
        
