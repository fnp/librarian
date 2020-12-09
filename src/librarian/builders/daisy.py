import subprocess
import tempfile
import zipfile
from aeneas.executetask import ExecuteTask
from aeneas.task import Task
from lxml import etree
import mutagen
from librarian import OutputFile, get_resource
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

    def build(self, document, mp3, **kwargs):
        if not mp3:
            raise ValueError("Need MP3 files")
        
        outfile = tempfile.NamedTemporaryFile(delete=False)
        zipf = zipfile.ZipFile(outfile, 'w')

        directory = document.meta.url.slug + '/'

        html = DaisyHtmlBuilder().build(document)
        zipf.write(
            html.get_filename(),
            directory + 'book.html',
        )

        durations = []
        for i, mp3_file in enumerate(mp3):
            durations.append(get_duration(mp3_file))
            zipf.write(
                mp3_file,
                directory + "book%d.mp3" % i,
            )
        duration = sum(durations)

        config_string = "task_language=pol|is_text_type=unparsed|is_text_unparsed_id_regex=sec\d+$|is_text_unparsed_id_sort=numeric|os_task_file_format=tab"
        task = Task(config_string=config_string)

        # TODO: concatenate all the
        with tempfile.TemporaryDirectory() as temp:
            with open(temp + "/book.mp3", "wb") as m:
                for minput in mp3:
                    with open(minput, "rb") as minputf:
                        m.write(minputf.read())
                
            
            syncfile = temp + "/sync"
            task.audio_file_path_absolute = temp + "/book.mp3"
            task.text_file_path_absolute = html.get_filename()
            task.sync_map_file_path_absolute = syncfile

            ExecuteTask(task).execute()
            task.output_sync_map_file()
            sync = []
            with open(syncfile) as f:
                for line in f:
                    start, end, sec = line.strip().split('\t')
                    start = float(start)
                    end = float(end)
                    sync.append([start, end, sec])

        hms = format_hms(duration)

        narrator = mutagen.File(mp3[0]).get('TPE1')
        narrator = narrator.text[0] if narrator else ''

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

        for fname in ('smil10.dtd', 'xhtml1-transitional.dtd', 'xhtml-lat1.ent', 'xhtml-special.ent', 'xhtml-symbol.ent'):
            zipf.write(
                get_resource('res/daisy/' + fname),
                directory + fname)

        for fname in ('er_book_info.xml', 'master.smil', 'ncc.html'):
            with open(get_resource('res/daisy/' + fname)) as f:
                tree = etree.parse(f)
            populate(tree.getroot(), context)
            zipf.writestr(
                directory + fname,
                etree.tostring(
                    tree,
                    xml_declaration=True
                ),
            )

        with open(get_resource('res/daisy/content.smil')) as f:
            tree = etree.parse(f)
        populate(tree.getroot(), context)

        seq = tree.find('//seq')
        for i, item in enumerate(sync):
            par = etree.SubElement(seq, 'par', id="par%06d" % (i + 1), endsync="last")
            etree.SubElement(
                par,
                "text",
                src="book.html#%s" % item[2])

            # If we have a split between mp3 parts, err on the larger side.
            i = 0
            start, end = item[0], item[1]
            while start >= durations[i]:
                start -= durations[i]
                end -= durations[i]
                i += 1
            if 2 * (end - durations[i]) > end - start:
                start = 0
                end -= durations[i]
                i += 1

            audio = etree.SubElement(
                par,
                "audio",
                src="book%d.mp3" % i,
                **{
                    "clip-begin": "npt=%.3fs" % start,
                    "clip-end": "npt=%.3fs" % end,
                },
            )
            
        zipf.writestr(
            directory + 'content.smil',
            etree.tostring(
                tree,
                xml_declaration=True,
                pretty_print=True,
            ),
        )

            
# WHERE IS MP3
        
        zipf.close()
        return OutputFile.from_filename(outfile.name)
