import unittest
import os


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.db_path = 'database/my_db.sqlite'

    def test_default_widget_size(self):
        self.assertEqual(os.path.exists(self.db_path), True, 'database file not found')


if __name__ == '__main__':
    unittest.main()
