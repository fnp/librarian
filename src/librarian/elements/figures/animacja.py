from ..base import WLElement


class Animacja(WLElement):
    HTML_TAG = 'div'
    HTML_CLASS = "animacja cycle-slideshow"
    HTML_ATTR = {
        "data-cycle-pause-on-hover": "true",
        "data-cycle-next": "> img",
        "data-cycle-fx": "fadeout",
        "data-cycle-paused": "true",
    }
