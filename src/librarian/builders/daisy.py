# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from copy import deepcopy
import subprocess
import tempfile
import zipfile
from lxml import etree
import mutagen
from librarian import OutputFile, get_resource
from librarian.html import raw_printable_text
from .html import DaisyHtmlBuilder


def get_duration(path):
    return float(
        subprocess.run(
            [
                "ffprobe",
                "-i",
                path,
                "-show_entries",
                "format=duration",
                "-v",
                "quiet",
                "-of",
                "csv=p=0",
            ],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )


def format_hms(t):
    seconds = t % 60
    t -= seconds
    t /= 60
    minutes = t % 60
    t -= minutes
    hours = t / 60
    return "%02d:%02d:%02.3f" % (hours, minutes, seconds)    


def populate(element, context):
    if element.text:
        element.text = element.text.format(**context)
    if element.tail:
        element.tail = element.tail.format(**context)
    for k, v in element.attrib.items():
        element.attrib[k] = v.format(**context)
    for child in element:
        populate(child, context)


class DaisyBuilder:
    file_extension = 'daisy.zip'

    def build(self, document, mp3, split_on=None, **kwargs):
        if not mp3:
            raise ValueError("Need MP3 files")
        
        outfile = tempfile.NamedTemporaryFile(delete=False)
        zipf = zipfile.ZipFile(outfile, 'w')

        directory = document.meta.url.slug + '/'

        if split_on:
            documents = []
            headers = []
            present = True
            n = 0
            while present:
                present = False
                n += 1
                newdoc = deepcopy(document)
                newdoc.tree.getroot().document = newdoc

                master = newdoc.tree.getroot()[-1]
                i = 0
                for item in list(master):
                    if item.tag == split_on:
                        # TODO: clear
                        i += 1
                        if i == n:
                            headers.append(raw_printable_text(item))
                    if i != n and not (n == 1 and not i):
                        master.remove(item)
                    else:
                        present = True
                if present:
                    documents.append(newdoc)
        else:
            documents = [document]
            headers = [document.meta.title]

        assert len(documents) == len(mp3)

        narrator = mutagen.File(mp3[0]).get('TPE1')
        narrator = narrator.text[0] if narrator else ''

        durations = []
        for i, part in enumerate(documents):
            print('part', i)
            html = DaisyHtmlBuilder().build(part)
            zipf.write(
                html.get_filename(),
                directory + 'book%d.html' % i,
            )

            durations.append(get_duration(mp3[i]))
            zipf.write(
                mp3[i],
                directory + "book%d.mp3" % i,
            )

            populate(tree.getroot(), context)

            zipf.write(
                syncfiles[i],
                directory + 'content%d.smil' % i,
            )

        for fname in ('smil10.dtd', 'xhtml1-transitional.dtd', 'xhtml-lat1.ent', 'xhtml-special.ent', 'xhtml-symbol.ent'):
            zipf.write(
                get_resource('res/daisy/' + fname),
                directory + fname)

        duration = sum(durations)
        hms = format_hms(duration)
        context = {
            "VERSION": "1.10",
            "HHMMSSmmm": hms,
            "HHMMSS": hms.split('.')[0],
            "Sd": "%.1f" % duration,
            "TITLE": document.meta.title,
            "PUBLISHER": document.meta.publisher[0],
            "YEAR": document.meta.created_at[:4],
            "MONTH": document.meta.created_at[5:7],
            "AUTHOR": document.meta.author.readable(),
            "NARRATOR": narrator,
        }

        tree = etree.parse(get_resource('res/daisy/er_book_info.xml'))
        cont = tree.getroot()[0]
        for i, dur in enumerate(durations):
            etree.SubElement(cont, 'smil', nr=str(i+1), Name="content%i.smil" % i, dur="%.1f" % dur)
        zipf.writestr(
            directory + 'er_book_info.xml',
            etree.tostring(tree, xml_declaration=True))

        tree = etree.parse(get_resource('res/daisy/master.smil'))
        populate(tree.getroot(), context)
        cont = tree.getroot()[-1]
        for i, header in enumerate(headers):
            etree.SubElement(cont, 'ref', title=header, src="content%d.smil#seq000001" % i, id="smil_%04d" % i)
        zipf.writestr(
            directory + 'master.smil',
            etree.tostring(tree, xml_declaration=True))

        tree = etree.parse(get_resource('res/daisy/ncc.html'))
        populate(tree.getroot(), context)
        cont = tree.getroot()[-1]
        for i, header in enumerate(headers):
            if not i:
                h1 = etree.SubElement(
                    cont, 'h1', id='content', **{"class": "title"})
                etree.SubElement(
                    h1, "a", href='content%d.smil#par000001' % i).text = document.meta.title
            else:
                h2 = etree.SubElement(
                    cont, 'h2', id='content', **{"class": "chapter"})
                etree.SubElement(
                    h2, "a", href='content%d.smil#par000001' % i).text = header

        zipf.writestr(
            directory + 'ncc.html',
            etree.tostring(tree, xml_declaration=True))

        zipf.close()
        return OutputFile.from_filename(outfile.name)
