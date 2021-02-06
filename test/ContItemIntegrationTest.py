import unittest
import gc
from lib.Container import Container
from lib.Item import Item


class ContItemIntegration(unittest.TestCase):
    container: Container
    itemSmaller: Item
    itemSame: Item
    itemLarger: Item

    def setUp(self) -> None:
        self.container = Container(0, 0, 0, 100, 100, 100)
        self.itemSmaller = Item(50, 50, 50, 5, "SMALLER")
        self.itemSame = Item(100, 100, 100, 5,  "SAME")
        self.itemLarger = Item(150, 150, 150, 5, "LARGER")

    def testIsSmaller1(self):
        self.assertEqual(self.container.is_smaller(self.itemSmaller), [True, True, True])

    def testIsSmaller2(self):
        self.assertEqual(self.container.is_smaller(self.itemSame), [True, True, True])

    def testIsSmaller3(self):
        self.assertEqual(self.container.is_smaller(self.itemLarger), [False, False, False])

    def testReservedSpace1_1(self):
        self.container.update_reserved_space(length=self.itemSmaller.get_length())
        self.assertEqual(self.container.reserved_length, 50)

    def testReservedSpace1_2(self):
        self.container.update_reserved_space(width=self.itemSmaller.get_width())
        self.assertEqual(self.container.reserved_width, 50)

    def testReservedSpace1_3(self):
        self.container.update_reserved_space(height=self.itemSmaller.get_height())
        self.assertEqual(self.container.reserved_height, 50)

    def testReservedSpace1_4(self):
        self.container.update_reserved_space(size=self.itemSmaller.get_size())
        self.assertEqual(self.container.reserved_size, [50, 50, 50])

    def testReservedSpace2_1(self):
        self.container.update_reserved_space(length=self.itemSame.get_length())
        self.assertEqual(self.container.reserved_length, 100)

    def testReservedSpace2_2(self):
        self.container.update_reserved_space(width=self.itemSame.get_width())
        self.assertEqual(self.container.reserved_width, 100)

    def testReservedSpace2_3(self):
        self.container.update_reserved_space(height=self.itemSame.get_height())
        self.assertEqual(self.container.reserved_height, 100)

    def testReservedSpace2_4(self):
        self.container.update_reserved_space(size=self.itemSame.get_size())
        self.assertEqual(self.container.reserved_size, [100, 100, 100])

    def testReservedSpace3_1(self):
        self.container.update_reserved_space(length=self.itemLarger.get_length())
        self.assertEqual(self.container.reserved_length, 0)

    def testReservedSpace3_2(self):
        self.container.update_reserved_space(width=self.itemLarger.get_width())
        self.assertEqual(self.container.reserved_width, 0)

    def testReservedSpace3_3(self):
        self.container.update_reserved_space(height=self.itemLarger.get_height())
        self.assertEqual(self.container.reserved_height, 0)

    def testReservedSpace3_4(self):
        self.container.update_reserved_space(size=self.itemLarger.get_size())
        self.assertEqual([0, 0, 0], self.container.reserved_size)

    # TODO: Make test for Container.add_item()

    def tearDown(self) -> None:
        del self.container
        del self.itemSmaller
        del self.itemSame
        del self.itemLarger
        gc.collect()


if __name__ == '__main__':
    unittest.main()
