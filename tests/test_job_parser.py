#from __future__ import absolute_import
from ..utils import job_parser
from ..utils import common
from nose2.tools import params
from nose2.tools import such
import unittest2 as unittest


class MyTestCase(unittest.TestCase):

    def test(self):
        self.assertRaises(Exception,job_parser.get_category_path,type_val='data',krama_root=None)

    def test2(self):
        self.assertRaises(Exception, job_parser.get_category_path, arg=None,type_val='data',
                      krama_root=None)


    def test3(self):
        self.assertRaises(Exception, common.is_empty_filename, 'hello')
