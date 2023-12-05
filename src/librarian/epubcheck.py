import json
import re
import subprocess
import zipfile


def epubcheck(filename):
    p = subprocess.run(
        [
            'epubcheck', '-q',
            '-j', '-',
            filename
        ],
        capture_output=True
    )
    output = json.loads(p.stdout)
    epub = zipfile.ZipFile(filename)
    messages = output.get('messages', [])
    for message in messages:
        for loc in message.get('locations', []):
            if loc['path'].startswith('EPUB/part'):
                with epub.open(loc['path']) as zfile:
                    text = zfile.read().decode('utf-8')
                line = text.split('\n')[loc['line'] - 1][:loc['column'] - 1:]
                debug = re.findall(r' data-debug="(\d+):(\d+)', line)
                if debug:
                    debug = debug[-1]
                    loc['wl_chunk'] = int(debug[0])
                    loc['wl_line'] = int(debug[1])
    return messages

            
        
