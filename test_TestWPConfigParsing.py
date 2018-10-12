from __future__ import with_statement
from __future__ import absolute_import
import WPBackup
import os
import unittest
from io import open

FIXTURE_DIRECTORY = u'fixture/wp_test'


class TestWPConfigParsing(unittest.TestCase):
    def test_parsing_wpconfig_invalid_content(self):
        result = WPBackup.parsing_wpconfig_content(u"")
        self.assertEqual({}, result)

    def test_parsing_wpconfig_null_content(self):
        result = WPBackup.parsing_wpconfig_content(None)
        self.assertEqual({}, result)

    def test_parsing_wpconfig_valid_content(self):
        path = os.path.abspath(os.path.dirname(__file__))
        config_path = os.path.join(path, FIXTURE_DIRECTORY + u'/wp-config.php')
        content = None
        with open(config_path, encoding=u"utf-8") as fh:
            content = fh.read()
        self.assertIsNotNone(content)
        result = WPBackup.parsing_wpconfig_content(content)
        self.assertEqual(u'dbname', result[u'database'])
        self.assertEqual(u'user', result[u'user'])
        self.assertEqual(u'password', result[u'password'])
        self.assertEqual(u'mysql.domain.xyz.de', result[u'host'])

    def test_parsing_wpconfig_valid_file(self):
        path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(path, FIXTURE_DIRECTORY)
        result = WPBackup.parsing_wpconfig(path)
        self.assertEqual(u'dbname', result[u'database'])
        self.assertEqual(u'user', result[u'user'])
        self.assertEqual(u'password', result[u'password'])
        self.assertEqual(u'mysql.domain.xyz.de', result[u'host'])
