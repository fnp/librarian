import PIL.Image
import PIL.ImageDraw


def split_words(text):
    words = []
    conj = False
    for word in text.split():
        if conj:
            words[-1] += ' ' + word
        else:
            words.append(word)
        conj = len(word.lstrip('(').lstrip('[')) == 1
    return words



def text_with_tracking(draw, tracking, pos, text, fill=None, font=None):
    x, y = pos
    for c in text:
        width = font.getsize(c)[0]
        draw.text((x, y), c, fill=fill, font=font)
        x += width + tracking


class DoesNotFit(Exception):
    pass


class TextBox:
    def __init__(self, width, height, texts,
                 font, lines, leading, tracking,
                 align_h, align_v):
        self.width = width
        self.height = height
        self.texts = texts
        self.font = font
        self.lines = lines
        self.leading = leading
        self.tracking = tracking
        self.align_h = align_h
        self.align_v = align_v

        self.margin_top = self.font.getbbox('l')[1]

        self.glue = self.get_length(' ')
        
        groups = [
            (self.get_length(word), word)
            for word in self.texts
        ]

        self.grouping = self.find_grouping(groups, self.lines, self.glue)
        if self.grouping is None:
            raise DoesNotFit()

    def get_length(self, text):
        return self.font.getlength(text) + self.tracking * len(text)
        
    def as_pil_image(self, color):
        img = PIL.Image.new('RGBA', (self.width, self.height + 2 * self.margin_top))
        draw = PIL.ImageDraw.ImageDraw(img)

        font_letter_height = self.font.getmetrics()[0] - self.margin_top

        y = self.align_v * (self.height - ((self.lines - 1) * self.leading + font_letter_height))
        for group in self.grouping:
            x = (self.width - group[0] + self.tracking) * self.align_h
            self.align_h *  - group[0] / 2
            for s, w in group[1]:
                text_with_tracking(
                    draw, self.tracking, (x, y),
                    w, fill=color, font=self.font
                )
                x += s + self.glue
            y += self.leading

        return img

    def find_grouping(self, groups, ngroups, glue):
        best = None
        best_var = None
        if not groups:
            return []

        mean = sum(g[0] for g in groups) + (len(groups) - ngroups) * glue
        if mean > self.width * ngroups:
            return None

        for grouping in self.all_groupings(groups, ngroups, glue):
            if max(g[0] for g in grouping) > self.width:
                continue
            var = sum((g[0] - mean) ** 2 for g in grouping)
            if best is None or best_var > var:
                best, best_var = grouping, var

        return best

    def all_groupings(self, groups, ngroups, glue):
        if len(groups) == 1:
            if ngroups == 1:
                yield [(groups[0][0], groups)]
            return
        next_groups = groups[1:]
        for grouping in self.all_groupings(next_groups, ngroups, glue):
            yield [
                (
                    groups[0][0] + glue + grouping[0][0],
                    [groups[0]] + grouping[0][1]
                )
            ] + grouping[1:]
        if ngroups > 1:
            for grouping in self.all_groupings(next_groups, ngroups - 1, glue):
                yield [
                    (groups[0][0], [groups[0]])
                ] + grouping
