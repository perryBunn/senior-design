import Item


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
    contents: list
        The items stored by the container

    Methods
    -------
    add_item(item)
        Adds an Item object to the contents of the container
    new_container()
        Adds a new nested container to itself
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
    contents = []

    def __init__(self, xIn, yIn, zIn, lengthIn, widthIn, heightIn):
        self.x = xIn
        self.y = yIn
        self.z = zIn
        self.position = [self.x, self.y, self.z]
        self.length = lengthIn
        self.width = widthIn
        self.height = heightIn
        self.size = [self.length, self.width, self.height]
        self.volume = self.length * self.width * self.height
        self.reserved_size = [self.reserved_length, self.reserved_width, self.reserved_height]
        self.available_volume = self.volume - self.reserved_volume

    def update_reserved_space(self, length: int = None, width: int = None, height: int = None,
                              size: [int, int, int] = None) -> bool:
        """
        Updated the reserved dimensions for the container.
        At least one argument is required.
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
                print('passed length')
                if not self.reserved_width + size[1] > self.width:
                    print('passed width')
                    if not self.reserved_height + size[2] > self.height:
                        print('passed height')
                        self.reserved_length += size[0]
                        self.reserved_width += size[1]
                        self.reserved_height += size[2]
                        self.reserved_size = [size[0], size[1], size[2]]
                        status = True
        return status

    def add_item(self, item: Item):
        # In theory only the first container will create 3 new containers, subsequent iterations will create 0-2
        res = self.is_smaller(item)
        if res[0]:
            # New container in the X dimension
            # TODO: Need to update the reserved_length
            # TODO: I dont know if this will make the correct changes that im thinking...
            self.update_reserved_space(length=item.__length)
            self.new_container(self.x + 1, self.y, self.z,
                               self.available_length(),
                               self.available_width(),
                               self.available_height())
        if res[1]:
            # New container in the Y dimension
            # TODO: Need to update the reserved_width
            self.update_reserved_space(width=item.__width)
            self.new_container(self.x, self.y + 1, self.z,
                               self.available_length(),
                               self.available_width(),
                               self.available_height())
        if res[2]:
            # New container in the Z dimension
            # TODO: Need to update the reserved_height
            self.update_reserved_space(height=item.__height)
            self.new_container(self.x, self.y, self.z + 1,
                               self.available_length(),
                               self.available_width(),
                               self.available_height())
        self.contents.append(item)

    def new_container(self, x, y, z, length, width, height):
        # TODO: What if new child container is at the same position as the parent?
        cont = Container(x, y, z, length, width, height)
        self.contents.append(cont)

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
