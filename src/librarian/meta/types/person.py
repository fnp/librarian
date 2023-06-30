# This file is part of Librarian, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Wolne Lektury. See NOTICE for more information.
#
from functools import total_ordering
from .base import MetaValue


@total_ordering
class Person(MetaValue):
    """Single person with last name and a list of first names."""
    def __init__(self, last_name, *first_names):
        self.last_name = last_name
        self.first_names = first_names

    @classmethod
    def from_text(cls, text):
        parts = [token.strip() for token in text.split(',')]
        if len(parts) == 1:
            surname = parts[0]
            names = []
        elif len(parts) != 2:
            raise ValueError(
                "Invalid person name. "
                "There should be at most one comma: \"%s\"."
                % text.encode('utf-8')
            )
        else:
            surname = parts[0]
            if len(parts[1]) == 0:
                # there is no non-whitespace data after the comma
                raise ValueError(
                    "Found a comma, but no names given: \"%s\" -> %r."
                    % (text, parts)
                )
            names = parts[1].split()
        return cls(surname, *names)

    def readable(self):
        return " ".join(self.first_names + (self.last_name,))

    def __eq__(self, right):
        return (self.last_name == right.last_name
                and self.first_names == right.first_names)

    def __lt__(self, other):
        return ((self.last_name, self.first_names)
                < (other.last_name, other.first_names))

    def __hash__(self):
        return hash((self.last_name, self.first_names))

    def __str__(self):
        if len(self.first_names) > 0:
            return '%s, %s' % (self.last_name, ' '.join(self.first_names))
        else:
            return self.last_name

    def __repr__(self):
        return 'Person(last_name=%r, first_names=*%r)' % (
            self.last_name, self.first_names
        )
