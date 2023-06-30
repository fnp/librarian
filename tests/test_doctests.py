import unittest
import doctest
import librarian.util
import librarian.epub
import librarian.meta.types.wluri
import librarian.pdf
import librarian.embeds.mathml


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(librarian.util))
    tests.addTests(doctest.DocTestSuite(librarian.epub))
    tests.addTests(doctest.DocTestSuite(librarian.meta.types.wluri))
    tests.addTests(doctest.DocTestSuite(librarian.pdf))
    tests.addTests(doctest.DocTestSuite(librarian.embeds.mathml))
    return tests
