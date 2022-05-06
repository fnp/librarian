import PIL.Image
from .base import Widget


class Marquise(Widget):
    segments = 4

    def __init__(self, cover, edge_top):
        self.edge_top = edge_top
        super().__init__(cover)

    def setup(self):
        self.slope_w = self.cover.m.width / self.segments / 2
        self.segment_h = self.cover.m.margin
        self.title_box_position = (
            self.cover.m.margin,
            self.cover.m.title_box_top
        )

    def get_points(self, w):
        tip_y = self.edge_top + self.segment_h
        points = [
            (0, 0),
            (w, 0),
            (w, tip_y),
        ]
        for i in range(self.segments - 1, 0, -1):
            points.extend([
                ((2 * i + 1) * self.slope_w, self.edge_top),
                (2 * i * self.slope_w, tip_y)
            ])
        points.extend([
            (self.slope_w, self.edge_top),
            (0, tip_y)
        ])
        return points

    def build(self, w, h):
        img = PIL.Image.new('RGBA', (
            round(w), round(self.edge_top + self.segment_h)
        ))
        draw = PIL.ImageDraw.ImageDraw(img)
        draw.polygon(
            self.get_points(w), fill=self.cover.color_scheme['rgb'])
        return img
