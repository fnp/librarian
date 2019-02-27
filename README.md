License
-------

  ![AGPL Logo](http://www.gnu.org/graphics/agplv3-155x51.png)

    Copyright © 2008-2019 Fundacja Nowoczesna Polska <fundacja@nowoczesnapolska.org.pl>

    For full list of contributors see AUTHORS file.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


About
------

Librarian converts XML-based markup language used by FNP for writing books to
other formats, which are more suitable for presentation.

Currently we support:

 * HTML4, XHTML 1.0 (?)
 * Plain text
 * EPUB (XHTML based)
 * MOBI
 * print-ready PDF
 * FB2

Other features:

 * extract DublinCore meta-data from documents;
 * extract marked "themes" from documents.


Dependencies
------------

 * lxml <http://codespeak.net/lxml/>, version 2.2 or later
 * additional PDF converter dependencies:
   * XeTeX with support for Polish language
   * TeXML <http://getfo.org/texml/>
   * recommended: morefloats LaTeX package, version >=1.0c
     for dealing with documents with many motifs in one paragraph.
     <http://www.ctan.org/tex-archive/help/Catalogue/entries/morefloats.html>


Installation
------------

Librarian uses standard Python distutils for packaging. After installing all the dependencies just run:

    python setup.py install

PDF converter also needs the Junicode-WL fonts (librarian/pdf/JunicodeWL-*.ttf) installed.
In Debian/Ubuntu, put those files in ~/.fonts/ and run `fc-cache'.

Usage
------

To convert a series of files to XHTML:

    book2html file1.xml [file2.xml ...]

To convert a series of files to plain text:

    book2txt file1.xml [file2.xml ...]

To convert a file to EPUB:

    book2epub file.xml

To convert a file to PDF:

    book2pdf file.xml

To extract book fragments marked as "theme":

    bookfragments file1.xml [file2.xml ...]
