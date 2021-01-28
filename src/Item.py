class Item:
    """
    This class is used to store information about a package

    Attributes
    ----------
    length, width, height: int
        Dimensions of the container object
    size: list
        A list of the container dimensions
    volume: int
        The total volume of the container
    serial_number: string
        The serial number of a package

    Methods
    -------
    get_length()
        Returns the length of the item
    get_width()
        Returns the width of the item
    get_height()
        Returns the height of the item
    get_size()
        Returns a list of the length, width, and height
    get_serial()
        Returns the serial_number of the item
    """

    length, width, height = 0, 0, 0
    size = [length, width, height]
    volume = length * width * height
    serial_number = ""

    def __init__(self, lengthIn, widthIn, heightIn, serialnumberIn):
        self.length = lengthIn
        self.width = widthIn
        self.height = heightIn
        self.serial_number = serialnumberIn

    def get_length(self):
        return self.length

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_size(self):
        return self.size

    def get_serial(self):
        return self.serial_number
