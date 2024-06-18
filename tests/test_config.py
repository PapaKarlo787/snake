import unittest
from config_lib import Config


class ConfigTests(unittest.TestCase):
    def general_part(self, fn):
        conf = Config(fn, {'win': {'x': 10, 'y': 7}}).result
        self.assertIn('win', conf)
        self.assertIn('x', conf['win'])
        self.assertIn('y', conf['win'])
        self.assertEqual(conf['win']['x'], 10)
        self.assertEqual(conf['win']['y'], 7)

    def rewritable(self, fn):
        with open(fn, 'r') as f:
            var = f.read()
        self.general_part(fn)
        with open(fn, 'r') as f:
            self.assertEqual("[win]\nx = 10\ny = 7\n\n", f.read())
        with open(fn, 'w') as f:
            f.write(var)

    def test_normal(self):
        self.general_part("tests/config_test_files/normal")

    def test_file_is_unavalable(self):
        self.general_part("tests/config_test_files/unavalable")

    def test_random(self):
        self.general_part("tests/config_test_files/random_data")

    def test_extra_lines(self):
        self.general_part("tests/config_test_files/extra_lines")

    def test_with_negative(self):
        self.rewritable("tests/config_test_files/with_negative")

    def test_wrong_file(self):
        self.rewritable("tests/config_test_files/wrong")

    def test_changed_file(self):
        conf = Config("tests/config_test_files/changed",
                      {'win': {'x': 10, 'y': 7}}).result
        self.assertIn('win', conf)
        self.assertIn('x', conf['win'])
        self.assertIn('y', conf['win'])
        self.assertEqual(conf['win']['x'], 20)
        self.assertEqual(conf['win']['y'], 15)

    def test_many_blocks(self):
        initial = {'win': {'x': 10, 'y': 7},
                   'space': {'x': 7, 'y': 5, 'z': 12}}
        conf = Config("tests/config_test_files/many_blocks", initial).result
        self.assertIn('win', conf)
        self.assertIn('x', conf['win'])
        self.assertIn('y', conf['win'])
        self.assertEqual(conf['win']['x'], 10)
        self.assertEqual(conf['win']['y'], 7)
        self.assertIn('space', conf)
        self.assertIn('x', conf['space'])
        self.assertIn('y', conf['space'])
        self.assertIn('z', conf['space'])
        self.assertEqual(conf['space']['x'], 7)
        self.assertEqual(conf['space']['y'], 5)
        self.assertEqual(conf['space']['z'], 12)


if __name__ == '__main__':
    unittest.main()
