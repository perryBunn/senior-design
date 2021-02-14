class Item:
    """
    This class is used to store information about a package

    Attributes
    ----------
    __length, __width, __height: int
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

    __length, __width, __height = -1, -1, -1
    __size = [__length, __width, __height]
    __volume = -1
    __mass = -1
    __serial_number = ""
    __rank = -1

    def __init__(self, lengthIn: int, widthIn: int, heightIn: int, massIn: int, serial_numberIn: str):
        self.__length = lengthIn
        self.__width = widthIn
        self.__height = heightIn
        self.__size = [self.__length, self.__width, self.__height]
        self.__volume = self.__length * self.__width * self.__height
        self.__mass = massIn
        self.__serial_number = serial_numberIn
        self.__rank = self.__volume * self.__mass

    def get_length(self) -> int:
        return self.__length

    def get_width(self) -> int:
        return self.__width

    def get_height(self) -> int:
        return self.__height

    def get_size(self) -> [int, int, int]:
        return self.__size

    def get_volume(self) -> int:
        return self.__volume

    def get_mass(self) -> int:
        return self.__mass

    def get_serial(self) -> str:
        return self.__serial_number

    def get_rank(self) -> int:
        return self.__rank

    def __str__(self):
        return f"Dimensions: {self.__size} Volume: {self.__volume} Mass: {self.__mass} Serial: {self.__serial_number}" \
               f" Rank: {self.__rank}"
