import WPBackup
import os
import unittest

FIXTURE_DIRECTORY = 'fixture/wp_test'


class TestWPConfigParsing(unittest.TestCase):
    def test_parsing_wpconfig_invalid_content(self):
        result = WPBackup.parsing_wpconfig_content("")
        self.assertEqual({}, result)

    def test_parsing_wpconfig_null_content(self):
        result = WPBackup.parsing_wpconfig_content(None)
        self.assertEqual({}, result)

    def test_parsing_wpconfig_valid_content(self):
        path = os.path.abspath(os.path.dirname(__file__))
        config_path = os.path.join(path, FIXTURE_DIRECTORY + '/wp-config.php')
        content = None
        with open(config_path, encoding="utf-8") as fh:
            content = fh.read()
        self.assertIsNotNone(content)
        result = WPBackup.parsing_wpconfig_content(content)
        self.assertEqual('dbname', result['database'])
        self.assertEqual('user', result['user'])
        self.assertEqual('password', result['password'])
        self.assertEqual('mysql.domain.xyz.de', result['host'])

    def test_parsing_wpconfig_valid_file(self):
        path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(path, FIXTURE_DIRECTORY)
        result = WPBackup.parsing_wpconfig(path)
        self.assertEqual('dbname', result['database'])
        self.assertEqual('user', result['user'])
        self.assertEqual('password', result['password'])
        self.assertEqual('mysql.domain.xyz.de', result['host'])
