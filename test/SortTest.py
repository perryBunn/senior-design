import unittest
import Sort

from lib.Container import Container


class SortTest(unittest.TestCase):
    container: Container

    def setUp(self) -> None:
        self.container = Container(0, 0, 0, 100, 100, 100)

    def testInsertionSort(self):
        sorted_list = []
        test_list = []
        Sort.insertion_sort()
        self.assertEqual(sorted_list, test_list)

    def tearDown(self) -> None:
        del self.container


if __name__ == '__main__':
    unittest.main()
