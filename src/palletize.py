from src.lib.Container import Container
from src.lib.Item import Item
from src.lib.Void import Void
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

    available_spaces = queue.Queue()
    pallet = Container(containerTemplate.x, containerTemplate.y, containerTemplate.z, containerTemplate.length,
                       containerTemplate.width, containerTemplate.height)
    available_spaces.put(pallet)
    available_space_size = 1
    item_pos = 0
    shipment = []
    smallest_size = items[len(items) - 1].get_size()
    while len(items) > 0:
        if available_space_size == 0:
            logging.info("Adding full pallet to shipment")
            shipment.append(pallet)
            logging.info("Creating new pallet")
            pallet = Container(containerTemplate.x, containerTemplate.y, containerTemplate.z, containerTemplate.length,
                               containerTemplate.width, containerTemplate.height)
            continue
        else:
            # Find most efficient orientation
            cur_container = available_spaces.get()  # <-- this gets the head of the queue
            cur_item = orient(items.pop(item_pos), cur_container)
            available_space_size -= 1
            cur_container.add_item(cur_item)
            cur_container.create_child(smallest_size)
            # Get new sub-containers and add to available_spaces
            for con in cur_container.children:
                if con.__class__.__name__ != "Void":
                    available_spaces.put(con)
                    available_space_size += 1

            logging.debug(cur_container)
            logging.debug(cur_container.item)
            logging.debug(available_space_size)
        # sort queue
        logging.debug(available_spaces)
    shipment.append(pallet)
    logging.debug("Items remaining: " + str(len(items)))
    logging.debug("Shipment size: " + str(available_space_size))
    return shipment


def orient(item: Item, container: Container) -> Item:
    """ Takes in a item and a container object. Based on the length and width of both objects will return the item
        orientation that leaves the best tiling possibilities.

    Parameters:
    item: Item
    container: Container

    Return:
    item: Item - Item in the correct orientation.
    """

    copy = item
    tiles_p = [0, 0]  # tiles in x, y
    tiles_l = [0, 0]

    # Portrait
    length = item.get_length()
    width = item.get_width()
    while (length*tiles_p[0]) < container.length:
        tiles_p[0] += 1
    while (width*tiles_p[1]) < container.width:
        tiles_p[1] += 1
    # Landscape
    copy.rotate()
    length = copy.get_length()
    width = copy.get_width()
    while length*tiles_l[0] < container.length:
        tiles_l[0] += 1
    while width*tiles_l[1] < container.width:
        tiles_l[1] += 1

    # Compare
    remain_por_x = container.length - (tiles_p[0]*item.get_length())
    remain_por_y = container.width - (tiles_p[1]*item.get_width())

    remain_lan_x = container.length - (tiles_l[0]*copy.get_length())
    remain_lan_y = container.width - (tiles_l[1]*copy.get_width())

    remain_por_area = (remain_por_x*container.width) + (remain_por_y*container.length) - (remain_por_y*remain_por_x)
    remain_lan_area = (remain_lan_x * container.width) + (remain_lan_y * container.length) - \
                      (remain_lan_y * remain_lan_x)

    if remain_por_area < remain_lan_area:
        return item
    elif remain_lan_area < remain_por_area:
        return copy
    else:
        # they have the same area, probably a square item
        # I dont think this well ever happen...
        logging.info("The remaining areas for portrait and landscape were the same. Returning the original item...")
        return item
