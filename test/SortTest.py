import math
import random
import unittest
import src.Sort as Sort
import src.lib.Item as Item
import src.lib.Container as Container


class SortTest(unittest.TestCase):
    container: Container
    length = 10000

    def setUp(self) -> None:
        self.container = Container(0, 0, 0, 100, 100, 100)

    def testInsertionSort(self):
        test_list = []
        for i in range(1, self.length):
            item = Item.Item(3 * i, 2 * i, i, i, f'{i}')
            test_list.append(item)
        random.shuffle(test_list)
        test_list = Sort.insertion(test_list, 0, test_list.__len__() - 1)
        prev = -1
        for item in test_list:
            if item.get_rank() > prev:
                prev = item.get_rank()
                continue
            else:
                assert False

    def testMergeSort(self):
        test_list = []
        for i in range(1, self.length):
            item = Item.Item(3 * i, 2 * i, i, i, f'{i}')
            test_list.append(item)
        random.shuffle(test_list)
        Sort.merge(test_list, 0, len(test_list))
        prev = -1
        for item in test_list:
            if item.get_rank() > prev:
                prev = item.get_rank()
                continue
            else:
                assert False

    def testTimSort(self):
        test_list = []
        for i in range(1, self.length):
            item = Item.Item(3 * i, 2 * i, i, i, f'{i}')
            test_list.append(item)
        random.shuffle(test_list)
        Sort.tim_sort(test_list)
        prev = -1
        for item in test_list:
            if item.get_rank() > prev:
                prev = item.get_rank()
                continue
            else:
                assert False

    def tearDown(self) -> None:
        del self.container


if __name__ == '__main__':
    unittest.main()
