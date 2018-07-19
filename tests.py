import unittest
import os
from sqlalchemy_model import create_database
import sqlalchemy_data as db


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        self.db = 'db_tests'
        self.db_path = 'database/{}.sqlite'.format(self.db)
        create_database(self.db)
        db.populate_database(self.db)

    def test_database_exists(self):
        self.assertEqual(os.path.exists(self.db_path), True, 'database file not found')

    def tearDown(self):
        os.remove(self.db_path)


if __name__ == '__main__':
    unittest.main()
