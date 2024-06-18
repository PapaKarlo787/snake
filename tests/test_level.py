import unittest
from level_lib import Level


class LevelTests(unittest.TestCase):
    def test_standrd_field(self):
        lev = Level(None, 5, 5)

    def test_3x3(self):
        lev = Level("tests/level_test_files/3x3", 5, 5)


if __name__ == '__main__':
    unittest.main()
