class Item:
    """
    This class is used to store information about a package

    Attributes
    ----------
    __length, __width, height: int
        Dimensions of the container object
    __size: list
        A list of the container dimensions
    __volume: int
        Volume of the item
    __mass: int
        Mass of the item
    __serial_number: str
        The serial number of a package

    Methods
    -------
    get_length() -> int:
        Returns the length of the item
    get_width() -> int:
        Returns the width of the item
    get_height() -> int:
        Returns the height of the item
    get_size() -> int:
        Returns a list of the length, width, and height
    get_volume() -> int:
        Returns the volume of the item
    get_mass() -> int:
        Returns the mass of the item
    get_serial() -> str:
        Returns the serial_number of the item
    """

    length, width, height = -1, -1, -1
    size = [length, width, height]
    __volume = -1
    __mass = -1
    __serial_number = ""
    __rank = -1

    def __init__(self, lengthIn: int, widthIn: int, heightIn: int, massIn: int, serial_numberIn: str):
        self.length = lengthIn
        self.width = widthIn
        self.height = heightIn
        self.size = [self.length, self.width, self.height]
        self.__volume = self.length * self.width * self.height
        self.__mass = massIn
        self.__serial_number = serial_numberIn
        # Rank can be a point of improvement
        self.__rank = (self.__volume * self.__mass)

    def get_length(self) -> int:
        return self.length

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_size(self) -> [int, int, int]:
        return self.size

    def get_volume(self) -> int:
        return self.__volume

    def get_mass(self) -> int:
        return self.__mass

    def get_serial(self) -> str:
        return self.__serial_number

    def get_rank(self) -> int:
        return self.__rank

    def __update_size(self):
        self.size = [self.length, self.width, self.height]

    def rotate(self) -> bool:
        """ Switches the length and width of the item. Returns a bool if successful.

        :return: Success
        """
        old_size = self.size
        self.width, self.length = self.length, self.width
        self.size = [self.length, self.width, self.height]

        if old_size == self.size:
            if self.width == self.length:
                pass
            else:
                raise ValueError
        return True

    def __str__(self):
        return f"Dimensions: {self.size} Volume: {self.__volume} Mass: {self.__mass} Serial: {self.__serial_number}" \
               f" Rank: {self.__rank}"
