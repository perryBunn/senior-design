import Item


class Container:
    """
    This class is used to store items

    Attributes
    ----------
    x, y, z : int
        Relative coordinates so that the container can be graphed
    position : list
        A list of the relative coordinates
    length, width, height: int
        Dimensions of the container object
    size: list
        A list of the container dimensions
    volume: int
        The total volume of the container
    contents: list
        The items stored by the container

    Methods
    -------
    add_item(item)
        Adds an Item object to the contents of the container
    add_new_container()
        Adds a new nested container to itself
    """

    x, y, z = 0, 0, 0
    position = [x, y, z]
    length, width, height = 0, 0, 0
    size = [length, width, height]
    volume = length * width * height
    reserved = 0
    available = volume - reserved
    contents = []

    def __init__(self, xIn, yIn, zIn, lengthIn, widthIn, heightIn):
        self.x = xIn
        self.y = yIn
        self.z = zIn
        self.length = lengthIn
        self.width = widthIn
        self.height = heightIn

    def add_item(self, item: Item):
        
        self.contents.append(item)

    def add_new_container(self):
        cont = Container()
        self.contents.append(cont)
