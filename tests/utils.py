from __future__ import with_statement

import os
from distutils.core import Command
from unittest import TextTestRunner, TestLoader
from glob import glob
from os.path import dirname, join, realpath, splitext, basename, walk
from os import listdir
import codecs

class AutoTestMetaclass(type):

    def __new__(cls, name, bases, class_dict):        
        test_dir = class_dict.pop('TEST_DIR')
        path = realpath( join(dirname(__file__), 'files', test_dir) )

        for file in listdir(path):
            base, ext = splitext(file)
            if ext != '.xml':
                continue

            class_dict['test_'+base] = cls.make_test_runner(base, \
                    join(path, base +'.xml'), join(path, base + '.out') )

        return type.__new__(cls, name, bases, class_dict)
    
    @staticmethod
    def make_test_runner(name, inputf, outputf):
        def runner(self):
            with open(inputf, 'rb') as ifd:
                with codecs.open(outputf, 'rb', encoding='utf-8') as ofd:
                    self.run_auto_test(ifd.read(), ofd.read())            
        return runner


def get_file_path(dir_name, file_name):
    return realpath(join(dirname(__file__), 'files', dir_name, file_name))

class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        '''
        Finds all the tests modules in tests/, and runs them.
        '''
        testfiles = []
        for t in glob(join(self._dir, 'tests', '*.py')):
            module_name = splitext(basename(t))[0]
            if module_name.startswith('test'):
                testfiles.append('.'.join(['tests', module_name])
                )

        tests = TestLoader().loadTestsFromNames(testfiles)
        t = TextTestRunner(verbosity=2)
        t.run(tests)

