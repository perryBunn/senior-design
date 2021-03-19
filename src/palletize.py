from src.lib.Container import Container
from src.lib.Item import Item
from src.lib.Void import Void
from collections import deque
import logging


def palletize(items: list, containerTemplate: Container) -> list:
    """ Takes in a list and a container object, will return a list of item queues. Will iterate through the item list
        and create queues of items to be packed. Once the first container is full it will create a new pallet.

    Parameters:
    items: list - List of items in packing list
    containerTemplate: Container - Template container for palletization. This is the base container that items will be
        put in. If there are more containers that need to be created it will be copies of this object.

    Return:
    pallets: list[deque] - List of item queues.
    """

    available_spaces = []
    pallet = Container(containerTemplate.x, containerTemplate.y, containerTemplate.z, containerTemplate.length,
                       containerTemplate.width, containerTemplate.height)
    available_spaces.append(pallet)
    available_space_size = 1
    item_pos = 0
    shipment = []
    smallest_size = items[len(items) - 1].get_size()
    while len(items) > 0:
        if available_space_size == 0:
            logging.info("Adding full pallet to shipment")
            shipment.append(extract(pallet))
            logging.info("Creating new pallet")
            pallet = None
            pallet = Container(containerTemplate.x, containerTemplate.y, containerTemplate.z, containerTemplate.length,
                               containerTemplate.width, containerTemplate.height)
            available_spaces.append(pallet)
            available_space_size += 1
            continue
        else:
            # Find most efficient orientation
            cur_container = available_spaces.pop()  # <-- this gets the head of the queue
            cur_item = orient(items.pop(item_pos), cur_container)
            available_space_size -= 1
            cur_container.add_item(cur_item)
            cur_container.create_child(smallest_size)
            # Get new sub-containers and add to available_spaces
            for con in cur_container.children:
                if con.__class__.__name__ != "Void":
                    available_spaces.append(con)
                    available_space_size += 1

            logging.debug(cur_container)
            logging.debug(cur_container.item)
            logging.debug(available_space_size)
        # sort queue
        sort_spaces(available_spaces)
        logging.debug(available_spaces)
    shipment.append(extract(pallet))
    logging.debug("Items remaining: " + str(len(items)))
    logging.debug("Shipment size: " + str(len(shipment)))

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
        # I dont think this well ever happen... Unless the container is square.
        logging.info("The remaining areas for portrait and landscape were the same. Returning the original item...")
        return item


def extract(pallet: Container):
    """ Will iterate through the container and add the items to the queue based on the coordinates of the package. It
        Needs to recurse through all of the packages and then based on those

    Z is the most important as the lower the Z the item must be packed first.

    :param pallet:
    :return:
    """
    print("Entering extract...")
    items = []
    # recurse through pallet
    items = extract_rec(pallet)
    print("Items: ", items)
    # Sort items
    sorted(items, key=lambda x: x.z)
    print(items[0].z, items[len(items) - 1].z)
    for i in items:
        print(i.x, i.y, i.z, i.item)
    print("Exiting extract...")
    return items


def extract_rec(pallet: Container):
    items = [pallet]
    if len(pallet.children) != 0:
        for child in pallet.children:
            if child.__class__.__name__ != "Void":
                temp = extract_rec(child)
                if type(temp) is list:
                    for i in temp:
                        items.append(i)
                else:
                    items.append(temp)
    return items


def sort_spaces(spaces: [Container]) -> list:
    """ Sorts the spaces based on level and available volume.

    Iterates through the list and first separates the spaces based on their Z values. then for each Z level sorts for
    most volume first.

    :param spaces:
    :return:
    """
    print("Entering sort_spaces...")
    levels: list[list[Container]] = [[]]
    for space in spaces:
        if space.z >= levels.__len__():
            while space.z >= levels.__len__():
                levels.append([])
            levels[space.z].append(space)
        else:
            levels[space.z].append(space)

    for level in levels:
        sorted(level, key=lambda x: x.z)

    result: list = []
    for level in levels:
        for container in level:
            result.append(container)
    print("Exiting sort_spaces...")
    return result
