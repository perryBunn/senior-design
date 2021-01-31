class Item:
    """
    This class is used to store information about a package

    Attributes
    ----------
    length, width, height: int
        Dimensions of the container object
    size: list
        A list of the container dimensions
    mass: int
        Mass of the item
    serial_number: str
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
    get_mass() -> int:
        Returns the mass of the item
    get_serial() -> str:
        Returns the serial_number of the item
    """

    length, width, height = 0, 0, 0
    size = [length, width, height]
    volume = length * width * height
    mass = 0
    serial_number = ""

    def __init__(self, lengthIn: int, widthIn: int, heightIn: int, massIn: int, serial_numberIn: str):
        self.length = lengthIn
        self.width = widthIn
        self.height = heightIn
        self.mass = massIn
        self.serial_number = serial_numberIn

    def get_length(self) -> int:
        return self.length

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_size(self) -> [int, int, int]:
        return self.size

    def get_mass(self) -> int:
        return self.mass

    def get_serial(self) -> str:
        return self.serial_number
