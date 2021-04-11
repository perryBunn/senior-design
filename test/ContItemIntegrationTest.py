import unittest
import gc
from src.lib.Container import Container
from src.lib.Item import Item


class ContItemIntegration(unittest.TestCase):
    container: Container
    itemSmaller: Item
    itemSame: Item
    itemLarger: Item

    def setUp(self) -> None:
        self.container = Container(0, 0, 0, [0, 0, 0], 100, 100, 100)
        self.itemSmaller = Item(50, 50, 50, 5, "SMALLER")
        self.itemSame = Item(100, 100, 100, 5,  "SAME")
        self.itemLarger = Item(150, 150, 150, 5, "LARGER")

    def testIsSmaller1(self):
        self.assertEqual(self.container.is_smaller(self.itemSmaller), [True, True, True])

    def testIsSmaller2(self):
        self.assertEqual(self.container.is_smaller(self.itemSame), [True, True, True])

    def testIsSmaller3(self):
        self.assertEqual(self.container.is_smaller(self.itemLarger), [False, False, False])

    # TODO: Make test for Container.add_item()

    def tearDown(self) -> None:
        del self.container
        del self.itemSmaller
        del self.itemSame
        del self.itemLarger
        gc.collect()


if __name__ == '__main__':
    unittest.main()
