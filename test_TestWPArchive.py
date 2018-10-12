from __future__ import absolute_import
import WPBackup
import os
import unittest

BACKUP_TEST_DIRECTORY = u'backup'
FIXTURE_DIRECTORY = u'fixture'


class TestWPConfigParsing(unittest.TestCase):
    def test_invalid_dump_file(self):
        path = os.path.abspath(os.path.dirname(__file__))
        backup_directory = os.path.join(path, BACKUP_TEST_DIRECTORY)
        self.assertIsNone(WPBackup.make_archive(
            u'wp1', u'', backup_directory))

    def test_invalid_wp_directory(self):
        path = os.path.abspath(os.path.dirname(__file__))
        backup_directory = os.path.join(path, BACKUP_TEST_DIRECTORY)
        self.assertIsNone(WPBackup.make_archive(
            u'', u'', backup_directory))

    def test_invalid_all(self):
        self.assertIsNone(WPBackup.make_archive(
            u'', u'', u''))

    def test_valid(self):
        path = os.path.abspath(os.path.dirname(__file__))
        backup_directory = os.path.join(path, BACKUP_TEST_DIRECTORY)
        test_file_path = os.path.join(path, FIXTURE_DIRECTORY + u'/dump.sql')
        wp_dir = os.path.join(path, FIXTURE_DIRECTORY + u'/wp_test')
        self.assertIsNotNone(WPBackup.make_archive(
            wp_dir, test_file_path, backup_directory))