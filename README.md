License
-------

  ![AGPL Logo](http://www.gnu.org/graphics/agplv3-155x51.png)
    
    Copyright © 2008,2009,2010 Fundacja Nowoczesna Polska <fundacja@nowoczesnapolska.org.pl>
    
    For full list of contributors see AUTHORS section at the end. 

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

 * HTML4, XHTML 1.0
 * Plain text 
 
In the future, we plan to support:

 * EPUB (XHTML based)
 * print-ready PDF 


Other features: 

 * extract DublinCore meta-data from documents;
 * extract marked "themes" from documents.


Dependencies
------------

 * lxml <http://codespeak.net/lxml/>, version 2.2 or later


Installation
------------

Librarian uses standard Python distutils for packaging. After installing all the dependencies just run:

    python setup.py install
    

Usage
------

To convert a series of file to XHTML:

    book2html file1.xml [file2.xml ...]

To convert a series of file to plain text:

    book2txt file1.xml [file2.xml ...]

To extract book fragments marked as "theme":

    bookfragments file1.xml [file2.xml ...]


Authors
-------
Originally written by Marek Stępniowski <marek@stepniowski.com>
	
Later contributions:

 * Łukasz Rekucki <lrekucki@gmail.com>
 * Radek Czajka <radek.czajka@gmail.com>