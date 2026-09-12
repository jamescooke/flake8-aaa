import unittest


class TestBad(unittest.TestCase):

    def test_subtest(self) -> None:  # noqa: AAA01
        for a in ['a']:
            with self.subTest(a=a):
                result = a.islower()

                self.assertTrue(result)

    def test_even(self) -> None:  # noqa: AAA
        """
        stdlib docs example: Test that numbers between 0 and 5 are all even.
        """
        for i in range(0, 6):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0)
