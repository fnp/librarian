from datetime import date
import re
import time
from .base import MetaValue


class DateValue(MetaValue):
    @classmethod
    def from_text(cls, text):
        """
        Dates for digitization of pictures. It seems we need the following:
        ranges:		'1350-1450',
        centuries:	"XVIII w.'
        half centuries/decades: '2 poł. XVIII w.', 'XVII w., l. 20'
        later-then: 'po 1450'
        circa 'ok. 1813-1814', 'ok.1876-ok.1886
        turn: 1893/1894

        For now we will translate this to some single date
        losing information of course.
        """
        try:
            # check out the "N. poł X w." syntax
            century_format = (
                "(?:([12]) *poł[.]? +)?([MCDXVI]+) *w[.,]*(?: *l[.]? *([0-9]+))?"
            )
            vague_format = "(?:po *|ok. *)?([0-9]{4})(-[0-9]{2}-[0-9]{2})?"

            m = re.match(century_format, text)
            m2 = re.match(vague_format, text)
            if m:
                half = m.group(1)
                decade = m.group(3)
                century = roman_to_int(m.group(2))
                if half is not None:
                    if decade is not None:
                        raise ValueError(
                            "Bad date format. "
                            "Cannot specify both half and decade of century."
                        )
                    half = int(half)
                    t = ((century*100 + (half-1)*50), 1, 1)
                else:
                    decade = int(decade or 0)
                    t = ((century*100 + decade), 1, 1)
            elif m2:
                year = m2.group(1)
                mon_day = m2.group(2)
                if mon_day:
                    t = time.strptime(year + mon_day, "%Y-%m-%d")
                else:
                    t = time.strptime(year, '%Y')
            else:
                raise ValueError

            return cls(date(t[0], t[1], t[2]))
        except ValueError:
            raise ValueError("Unrecognized date format. Try YYYY-MM-DD or YYYY.")
