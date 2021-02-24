from src.lib.Item import Item


class ItemOverwriteError(Exception):
    """
    Exception raised for errors where an Item addition would overwrite an existing item.

    Attributes:
    -----------
    message: str
        Message of the error that occurred
    """

    item: Item
    message: str = ""

    def __init__(self, item: Item, message: str = "Item already exist in this container."):
        self.item = item
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.item} -> {self.message}'
