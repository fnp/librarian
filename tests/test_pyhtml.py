# -*- coding: utf-8 -*-
from librarian import xmlutils
from lxml import etree
from librarian.pyhtml import EduModule
from nose.tools import *
from tests.utils import get_fixture


def test_traversal():
    xml = etree.fromstring("<a><b>BBBB</b><c>CCCC</c></a>")
    hg = xmlutils.Xmill()
    assert_equals(hg.next(xml), xml[0])
    assert_equals(hg.next(xml[0]), xml[1])
    assert_equals(hg.next(xml[1]), None)


class Foo(xmlutils.Xmill):
    def __init__(self):
        super(Foo, self).__init__()
        self.mode = 0

    def handle_title(self, ele):
        return "Title: ``%s''" % ele.text

    def handle_artist(self, ele):
        return "Artist: %s" % ele.text

    def handle_song(self, ele):
        if ele.getnext() is not None:
            return "\n", "--------------------\n"


def test_xml_generation():
    xml = u"""<root>
        <songs>
        <song>
        <title>Oursoul</title>
        <artist>Hindi Zahra</artist>
        </song>
        <song>
        <title>Visitor</title>
        <artist>Portico Quartet</artist>
        </song>
        </songs>
        </root>
    """
    txt = Foo().generate(etree.fromstring(xml))
    print txt


def test_edumodule():
    xml = open(get_fixture('edumed', 'gim-wizerunek-w-sieci.xml')).read()
    em = EduModule()
    out = em.generate(etree.fromstring(xml))
    print out.encode('utf-8')
