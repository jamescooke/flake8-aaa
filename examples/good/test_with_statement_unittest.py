import io
import pathlib
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        self.hello_world_path = pathlib.Path(__file__).parent.parent / 'data' / 'hello_world.txt'

    def test_assert_raises_in_block(self):
        """
        Checking on a raise in a with block works with unittest.
        """
        with open(self.hello_world_path) as f:

            with self.assertRaises(io.UnsupportedOperation):
                f.write('hello back')

            self.assertEqual(f.read(), 'Hello World!\n')

    def test_assert_raises_on_with(self):
        """
        Checking on the raise from a with statement works with Pytest.
        """
        with self.assertRaises(ValueError) as cm:
            with open(self.hello_world_path, 'zz'):
                pass

        self.assertIn('invalid mode', str(cm.exception))
