import math
import random
import unittest
import Sort

from lib.Container import Container


class SortTest(unittest.TestCase):
    container: Container
    length = 1000

    def setUp(self) -> None:
        self.container = Container(0, 0, 0, 100, 100, 100)

    def testInsertionSort(self):
        sorted_list = []
        test_list = []
        for i in range(0, self.length):
            sorted_list.append(i)
        for i in range(0, self.length):
            test_list.append(i)
        random.shuffle(test_list)
        test_list = Sort.insertion(test_list, 0, test_list.__len__() - 1)
        self.assertEqual(sorted_list, test_list)

    def testMergeSort(self):
        sorted_list = []
        test_list = []
        for i in range(0, self.length):
            sorted_list.append(i)
        for i in range(0, self.length):
            test_list.append(i)
        random.shuffle(test_list)
        Sort.merge(test_list, 0, len(test_list))
        self.assertEqual(sorted_list, test_list)

    def testTimSort(self):
        sorted_list = []
        test_list = []
        for i in range(0, self.length):
            sorted_list.append(i)
        for i in range(0, self.length):
            test_list.append(i)
        random.shuffle(test_list)
        Sort.tim_sort(test_list)
        self.assertEqual(sorted_list, test_list)

    def tearDown(self) -> None:
        del self.container


if __name__ == '__main__':
    unittest.main()
