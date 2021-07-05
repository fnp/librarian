import os
from shutil import rmtree
import subprocess
from tempfile import mkdtemp


def strip_font(path, chars, verbose=False):
    tmpdir = mkdtemp('-librarian-epub')
    try:
        cwd = os.getcwd()
    except OSError:
        cwd = None

    os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                          'font-optimizer'))
    optimizer_call = [
        'perl', 'subset.pl', '--chars',
        ''.join(chars).encode('utf-8'),
        path,
        os.path.join(tmpdir, 'font.ttf')
    ]
    env = {"PERL_USE_UNSAFE_INC": "1"}
    if verbose:
        print("Running font-optimizer")
        subprocess.check_call(optimizer_call, env=env)
    else:
        dev_null = open(os.devnull, 'w')
        subprocess.check_call(optimizer_call, stdout=dev_null,
                              stderr=dev_null, env=env)
    with open(os.path.join(tmpdir, 'font.ttf'), 'rb') as f:
        content = f.read()

    rmtree(tmpdir)

    if cwd is not None:
        os.chdir(cwd)

    return content
