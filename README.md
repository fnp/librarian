Licence
=======
    
    Copyright © 2008,2009,2010 Fundacja Nowoczesna Polska <fundacja@nowoczesnapolska.org.pl>
    
    For full list of contibutors see AUTHORS section at the end. 

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


Librarian
=========

Librarian (*ang. bibliotekarz*) to biblioteka służąca do konwersji języka składu książek opartego na XML opracowanego przez Fundację Nowoczesna Polska na inne formaty.

Obecnie obsługiwane są formaty:

 * XML
 * TXT
 
Biblioteka librarian potrafi również parsować metadane opisane przez DublinCore oraz wyciągać fragmenty motywów z lektur.


Wymagania
---------

 * [lxml 2.2](http://codespeak.net/lxml/)

 
Instalacja
----------
Zainstaluj biblioteki z sekcji *Wymagania* powyżej. Następnie rozpakuj archiwum z biblioteką librarian, przejdź w terminalu do rozpakowanego katalogu i wpisz:

<pre>python setup.py install</pre>

Na Linuxie i OSX mogą być wymagane uprawnienia administratora. W takim wypadku wpisz:

<pre>sudo python setup.py install</pre>

Alternatywnie możesz zainstalować bibliotekę librarian w wybranym przez siebie katalogu. W takim wypadku należy użyć argumentu *prefix* do *setup.py*:

<pre>python setup.py install --prefix=ŚCIEŻKA_DO_WYBRANEGO_KATALOGU</pre> 

W takim wypadku będzie jednak potrzebne własnoręczne edytowanie zmiennych systemowych *PATH* i *PYTHONPATH*.


Sposób użycia
-------------
Konwersja plików lektur do XHTML:

<pre>book2html LEKTURA1 LEKTURA2...</pre>

Konwersja plików lektur do TXT:

<pre>book2txt LEKTURA1 LEKTURA2...</pre>

Wyciągnięcie wszystkich fragmentów motywów z wygenerowanych plików XHTML:

<pre>bookfragments PLIK1 PLIK2...</pre>

Authors
-------
Originally written by Marek Stępniowski <marek@stepniowski>;
	
Later contributions:
    Łukasz Rekucki <lrekucki@gmail.com>




