class Void:
    """
    This class is to represent 3D space where it is too small to contain any item

    Attributes:
    -----------
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
    """
    x, y, z = 0, 0, 0
    position = [x, y, z]
    length, width, height = -1, -1, -1
    size = [length, width, height]
    volume = -1

    def __init__(self, x, y, z, length, width, height):
        self.x = x
        self.y = y
        self.z = z
        self.position = [self.x, self.y, self.z]
        self.length = length
        self.width = width
        self.height = height
        self.size = [self.length, self.width, self.height]
        self.volume = self.length * self.width * self.height
