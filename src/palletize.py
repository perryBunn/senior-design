from lib.Container import Container
from lib.Item import Item
from lib.Void import Void
import queue
import logging


def palletize(items: list, containerTemplate: Container) -> list[queue]:
    """ Takes in a list and a container object, will return a list of item queues. Will iterate through the item list
        and create queues of items to be packed. Once the first container is full it will create a new pallet.

    Parameters:
    items: list - List of items in packing list
    containerTemplate: Container - Template container for palletization. This is the base container that items will be
        put in. If there are more containers that need to be created it will be copies of this object.

    Return:
    pallets: list[queue] - List of item queues.
    """

    available_space_size = 0
    available_spaces = queue.Queue()
    pallet = Container(containerTemplate.x, containerTemplate.y, containerTemplate.z, containerTemplate.length,
                       containerTemplate.width, containerTemplate.height)
    item_pos = 0
    pallets = []
    smallest_size = items[len(items)-1].get_size()
    while len(items) > 0:
        # If available_spaces is empty then put item in container
        if available_space_size < 1:
            # Find most efficient orientation
            # cur_item = orient(items.pop(item_pos), pallet)
            cur_item = items.pop(item_pos)  # TODO: Delete this
            pallet.add_item(cur_item)
            pallet.create_child(smallest_size)
            # Get new sub-containers and add to available_spaces
            for con in pallet.children:
                if type(con) is not Void:
                    available_spaces.put(con)
                    available_space_size += 1
            logging.debug(pallet)
        else:
            raise NotImplementedError

    return pallets


def orient(item: Item, container: Container) -> Item:
    """ Takes in a item and a container object. Based on the length and width of both objects will return the item
        orientation that leaves the best tiling possibilities.

    NEED TO IMPLEMENT ITEM.ROTATE()

    Parameters:
    item: Item
    container: Container

    Return:
    item: Item - Item in the correct orientation.
    """
    raise NotImplementedError
