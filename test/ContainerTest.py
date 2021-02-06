import unittest

from lib.Container import Container


class ContainerTest(unittest.TestCase):
    container: Container

    def setUp(self) -> None:
        self.container = Container(0, 0, 0, 100, 100, 100)

    def testX(self):
        self.assertEqual(self.container.x, 0)

    def testY(self):
        self.assertEqual(self.container.y, 0)

    def testZ(self):
        self.assertEqual(self.container.z, 0)

    def testPosition(self):
        self.assertEqual(self.container.position, [0, 0, 0])

    def testLength(self):
        self.assertEqual(self.container.length, 100)

    def testWidth(self):
        self.assertEqual(self.container.width, 100)

    def testHeight(self):
        self.assertEqual(self.container.height, 100)

    def testSize(self):
        self.assertEqual(self.container.size, [100, 100, 100])

    def testVolume(self):
        self.assertEqual(self.container.volume, 1000000)

    def testReservedLength(self):
        self.assertEqual(self.container.reserved_length, 0)

    def testReservedWidth(self):
        self.assertEqual(self.container.reserved_width, 0)

    def testReservedHeight(self):
        self.assertEqual(self.container.reserved_height, 0)

    def testReservedSize(self):
        self.assertEqual(self.container.reserved_size, [0, 0, 0])

    def testReservedVolume(self):
        self.assertEqual(self.container.reserved_volume, 0)

    def testAvailableVolume(self):
        self.assertEqual(self.container.available_volume, 1000000)

    def testContentsEmpty(self):
        self.assertEqual(self.container.contents, [])

    def testAvailableLength(self):
        self.assertEqual(self.container.available_length(), 100)

    def testAvailableWidth(self):
        self.assertEqual(self.container.available_width(), 100)

    def testAvailableHeight(self):
        self.assertEqual(self.container.available_height(), 100)

    def testAvailableSize(self):
        self.assertEqual(self.container.available_size(), [100, 100, 100])

    def testNewContainer(self):
        self.container.add_container(1, 0, 0, 50, 50, 50)
        self.assertEqual(self.container.contents[0].length, 50)

    def tearDown(self) -> None:
        del self.container


if __name__ == '__main__':
    unittest.main()
