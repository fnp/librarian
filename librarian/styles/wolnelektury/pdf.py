import shutil
from librarian import get_resource
from librarian.pdf import PDFFormat
from librarian.styles.wolnelektury.cover import WLCover

class WLPDFFormat(PDFFormat):
    cover_class = WLCover
    style = get_resource('res/styles/wolnelektury/pdf/wolnelektury.sty')

    def get_tex_dir(self):
        temp = super(WLPDFFormat, self).get_tex_dir()
        shutil.copy(get_resource('res/wl-logo.png'), temp)
        return temp
