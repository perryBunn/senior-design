from lib.Item import Item
from lib.Void import Void
from lib.ItemOverwriteError import ItemOverwriteError


class Container:
    """
    This class is used to store items

    Attributes
    ----------
    x, y, z: int
        Relative coordinates so that the container can be graphed
    position: list
        A list of the relative coordinates
    length, width, height: int
        Dimensions of the container object
    size: list
        A list of the container dimensions
    volume: int
        The total volume of the container
    reserved_length, reserved_width, reserved_height: int
        Dimensions of the container object that are occupied by the contents
    reserved_size: list
        A list of the dimension occupied by Items
    reserved_volume: int
        The volume of the container that is directly occupied by the Items
    available_volume: int
        The free volume of the container that is not occupied by items
    item: Item
        The item stored by the container
    children: list
        The child containers of the container

    Methods
    -------
    update_reserved_space(int, int, int, [int, int, int]) -> bool:
        Updated the reserved space of the container. This will most likely get removed.
    create_child([int, int, int], Item):
        Will create child Containers and Voids based on the Item in the parent and smallest possible item
    add_item(Item):
        Adds an Item object to the contents of the container
    add_container():
        Adds a new child container to itself
    add_void():
        Adds a new child void to itself
    is_smaller(item) -> list:
        Checks to see if the item is smaller than the container
    available_length() -> int:
        Returns the available length of the container
    available_width() -> int:
        Returns the available width of the container
    available_height() -> int:
        Returns the available height of the container
    available_size() -> list:
        Returns a list of the available dimensions of the container
    """

    x, y, z = 0, 0, 0
    position = [x, y, z]
    length, width, height = -1, -1, -1
    size = [length, width, height]
    volume = -1
    reserved_length, reserved_width, reserved_height = 0, 0, 0
    reserved_size = [reserved_length, reserved_width, reserved_height]
    reserved_volume = 0
    available_volume = -1
    item = None
    children = []

    def __init__(self, x, y, z, length, width, height, item: Item = None):
        self.x = x
        self.y = y
        self.z = z
        self.position = [self.x, self.y, self.z]
        self.length = length
        self.width = width
        self.height = height
        self.size = [self.length, self.width, self.height]
        self.volume = self.length * self.width * self.height
        self.reserved_size = [self.reserved_length, self.reserved_width, self.reserved_height]
        self.available_volume = self.volume - self.reserved_volume
        if item is not None:
            self.item = item

    def update_reserved_space(self, length: int = None, width: int = None, height: int = None,
                              size: [int, int, int] = None) -> bool:
        """
        Updated the reserved dimensions for the container.
        At least/most one argument is required.
        :param length: Side length to be added to the reserved length
        :param width: Side length to be added to the reserved width
        :param height: Side length to be added to the reserved height
        :param size: List of side lengths to be added to the reserved dimensions
        :return: Returns if the operation was successful
        """
        status = False
        if length is not None:
            if not self.reserved_length + length > self.length:
                self.reserved_length += length
                self.reserved_size[0] = self.reserved_length
                status = True
        if width is not None:
            if not self.reserved_width + width > self.width:
                self.reserved_width += width
                self.reserved_size[1] = self.reserved_width
                status = True
        if height is not None:
            if not self.reserved_height + height > self.height:
                self.reserved_height += height
                self.reserved_size[2] = self.reserved_height
                status = True
        if size is not None:
            if not self.reserved_length + size[0] > self.length:
                if not self.reserved_width + size[1] > self.width:
                    if not self.reserved_height + size[2] > self.height:
                        self.reserved_length += size[0]
                        self.reserved_width += size[1]
                        self.reserved_height += size[2]
                        self.reserved_size = [size[0], size[1], size[2]]
                        status = True
        return status

    def create_child(self, smallest_possible_fit: [int, int, int], item: Item = None):
        """ Visualization
        Top looking down                          Y-axis looking at X     X-axis looking at Y
        (0,0,0) x--------------------             ------------------      ------------------
                | Item    | Child x |             | Child z        |      | Child z        |
                |         |         |             |                |      |                |
                -----------         |             |                |      |                |
                |         |         |             ------------------      ------------------
                | Child y |         |             | Item | Child y |      | Child x | Item |
                |         |         |             |      |         |      |         |      |
                ---------------------     (0,0,0) x-----------------      -----------------x (0,0,0)
        """
        if type(self) is not Void:
            if item is None:  # There is an item in the container
                available_length = self.length - self.item.get_length()
                available_width = self.width - self.item.get_width()
                available_height = self.height - self.item.get_height()

                # New container in the X dimension
                if available_length >= smallest_possible_fit[0]:
                    self.add_container(self.x + 1, self.y, self.z, available_length, self.width, self.item.get_height())
                else:
                    self.add_void(self.x + 1, self.y, self.z, available_length, self.width, self.item.get_height())

                # New container in the Y dimension
                if available_width >= smallest_possible_fit[1]:
                    self.add_container(self.x, self.y + 1, self.z, self.item.get_length(), available_width, self.item.get_height())
                else:
                    self.add_void(self.x, self.y + 1, self.z, self.item.get_length(), available_width, self.item.get_height())

                if available_height >= smallest_possible_fit[2]:
                    self.add_container(self.x, self.y, self.z + 1, self.length, self.width, available_height)
                else:
                    self.add_void(self.x, self.y, self.z + 1, self.length, self.width, available_height)
            else:  # There is not an item in the container
                available_length = self.length - item.get_length()
                available_width = self.width - item.get_width()
                available_height = self.height - item.get_height()

                # New container in the X dimension
                if available_length >= smallest_possible_fit[0]:
                    self.add_container(self.x + 1, self.y, self.z, available_length, self.width, item.get_height())
                else:
                    self.add_void(self.x + 1, self.y, self.z, available_length, self.width, item.get_height())

                # New container in the Y dimension
                if available_width >= smallest_possible_fit[1]:
                    self.add_container(self.x, self.y + 1, self.z, item.get_length(), available_width,
                                       item.get_height())
                else:
                    self.add_void(self.x, self.y + 1, self.z, item.get_length(), available_width, item.get_height())

                if available_height >= smallest_possible_fit[2]:
                    self.add_container(self.x, self.y, self.z + 1, self.length, self.width, available_height)
                else:
                    self.add_void(self.x, self.y, self.z + 1, self.length, self.width, available_height)

    def add_item(self, item: Item):
        if self.item is not None:
            raise ItemOverwriteError(self.item)
        else:
            self.item = item

    def add_container(self, x, y, z, length, width, height):
        # TODO: What if new child container is at the same position as the parent?
        # TODO: What if the parent container already has 3 children?
        cont = Container(x, y, z, length, width, height)
        self.children.append(cont)

    def add_void(self, x, y, z, length, width, height):
        # TODO: What if new child void is at the same position as the parent?
        # TODO: What if the parent container already has 3 children?
        void = Void(x, y, z, length, width, height)
        self.children.append(void)

    def is_smaller(self, item: Item) -> [bool, bool, bool]:
        res = [False, False, False]
        if item.get_length() <= self.length:
            res[0] = True
        if item.get_width() <= self.width:
            res[1] = True
        if item.get_height() <= self.height:
            res[2] = True
        return res

    def available_length(self) -> int:
        return self.length - self.reserved_length

    def available_width(self) -> int:
        return self.width - self.reserved_width

    def available_height(self) -> int:
        return self.height - self.reserved_height

    def available_size(self) -> [int, int, int]:
        return [self.available_length(), self.available_width(), self.available_height()]

    def __str__(self):
        res = f"Dimensions: {self.size}\nItem: {self.item}\nChild-Containers:"
        if len(self.children) > 0:
            for i in self.children:
                res += f"\n\t+- {type(i)}"
        else:
            res += "\n\t+- None"
        return res
