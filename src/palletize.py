from src.lib.Container import Container
from src.lib.Item import Item
from src.lib.Void import Void
import logging
import math


def palletize(items: list, containerTemplate: Container) -> list:
    """ Takes in a list and a container object, will return a list of item list. Will iterate through the item list
        and create list of items to be packed. Once the first container is full it will create a new pallet.

    Parameters:
    items: list - List of items in packing list
    containerTemplate: Container - Template container for palletization. This is the base container that items will be
        put in. If there are more containers that need to be created it will be copies of this object.

    Return:
    pallets: list[list] - List of list of items.
    """

    available_spaces = []
    pallet = Container(containerTemplate.x, containerTemplate.y, containerTemplate.z, containerTemplate.logi_coord, containerTemplate.length,
                       containerTemplate.width, containerTemplate.height)
    available_spaces.append(pallet)
    available_space_size = 1
    item_pos = 0
    shipment = []
    smallest_size = items[len(items) - 1].get_size()
    smallest_flag = False
    while len(items) > 0:
        logging.debug("===============================================================================================")
        logging.debug(f"Num Items: {len(items)} Item Pos: {item_pos} flag: {smallest_flag}")
        if item_pos == len(items):
            smallest_flag = True

        if smallest_flag:
            smallest_flag = False
            print(f"Available Spaces: {len(available_spaces)} {available_space_size} flag: {smallest_flag}")
            if len(available_spaces) >= 1:
                available_spaces.pop(0)
                available_space_size -= 1
            item_pos = 0
            if len(items) != 0:
                smallest_size = update_smallest(items, smallest_size)

        if len(available_spaces) == 0:
            logging.info(f"Available space: {available_space_size} flag: {smallest_flag}")
            logging.info("Adding full pallet to shipment")
            logging.debug("Items remaining: " + str(len(items)))
            pallet_ext = extract(pallet)
            logging.debug("Items packed in pallet: " + str(len(pallet_ext)))
            shipment.append(pallet_ext)
            logging.debug("Shipment size: " + str(len(shipment)))
            logging.debug("Creating new pallet")
            pallet = None
            pallet = Container(containerTemplate.x, containerTemplate.y, containerTemplate.z, containerTemplate.logi_coord, containerTemplate.length,
                               containerTemplate.width, containerTemplate.height)
            available_spaces.append(pallet)
            available_space_size += 1

            continue
        else:
            # Find most efficient orientation
            cur_container = available_spaces.pop(0)  # <-- this gets the head of the list
            cur_item = items.pop(item_pos)
            cur_item = orient(cur_item, cur_container)  # Rotates item for most insertions of same item type
            available_space_size -= 1
            logging.debug("Container: " + cur_container.__str__())
            logging.debug("Item: " + cur_item.__str__())
            # Check if item fits in container
            fit = cur_container.is_smaller(cur_item)
            if not fit[0] or not fit[1] or not fit[2]:
                logging.debug(f"Fit: {fit[0]} {fit[1]} {fit[2]}")
                logging.debug(f"Current: {cur_container} {cur_item}")
                logging.debug(f"Len_items, item_pos: {len(items)} {item_pos}")
                logging.debug(f"Available containers: {available_space_size}")

                items.append(cur_item)
                available_spaces.insert(0, cur_container)
                available_space_size += 1
                item_pos += 1
                continue
            cur_container.add_item(cur_item)
            cur_container.create_child(smallest_size)
            # Get new sub-containers and add to available_spaces
            for con in cur_container.children:
                if con.__class__.__name__ != "Void":
                    available_spaces.append(con)
                    available_space_size += 1
            logging.debug("Available Space list of dimensions:")
            for i in available_spaces:
                logging.debug(str(i.size))
            item_pos = 0

            logging.debug("Avail_space: " + str(available_space_size))
        # sort list
        sort_spaces(available_spaces)
        logging.debug(available_spaces)
        if available_space_size % 10 == 0:
            purge_available_smallest(available_spaces, smallest_size)
        if len(items) != 0:
            smallest_size = update_smallest(items, smallest_size)
    logging.debug("Items remaining: " + str(len(items)))
    logging.debug("Shipment size: " + str(len(shipment)))
    shipment.append(extract(pallet))

    return shipment


def purge_available_smallest(spaces: [Container], smallest):
    logging.debug("Entering Purge()...")
    pos = 0
    for cont in spaces:
        logging.debug(f"{pos} {len(spaces)} {cont.size} {smallest}")
        if cont.length < smallest[0]:
            temp = spaces.pop(pos)
            print("Purged: ", temp)
            continue
        if cont.width < smallest[1]:
            temp = spaces.pop(pos)
            print("Purged: ", temp)
            continue
        if cont.height < smallest[2]:
            temp = spaces.pop(pos)
            print("Purged: ", temp)
            continue
        pos += 1
    logging.debug("Exiting Purge()...")


def update_smallest(items, smallest: [int, int, int]) -> [int, int, int]:
    edit = False
    for item in items:
        side = math.inf
        if item.length < item.width:
            side = item.length
        else:
            side = item.width

        if side < smallest[0]:
            edit = True
            smallest[0] = side
            smallest[1] = side
        if item.height < smallest[2]:
            edit = True
            smallest[2] = item.height
    if edit is True:
        logging.info("New smallest item: " + str(smallest))
    return smallest


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
    item_area = item.get_length() * item.get_width()
    consumed_area_land = ((tiles_l[0]-1) * item_area) * (tiles_l[1]-1)
    consumed_area_port = ((tiles_p[0]-1) * item_area) * (tiles_p[1]-1)

    remain_lan_area = (container.length*container.width) - consumed_area_land
    remain_por_area = (container.length*container.width) - consumed_area_port

    if remain_por_area < remain_lan_area:
        return item
    elif remain_lan_area < remain_por_area:
        return copy
    else:
        # they have the same area, probably a square item
        logging.info("The remaining areas for portrait and landscape were the same. Returning the original item...")
        logging.info(str(item))
        return item


def extract(pallet: Container):
    """ Will iterate through the container and add the items to the list based on the coordinates of the package. It
        Needs to recurse through all of the packages and then based on those

    Z is the most important as the lower the Z the item must be packed first.

    :param pallet:
    :return:
    """
    items = []
    # recurse through pallet
    items = extract_rec(pallet)
    # Sort items
    sorted(items, key=lambda x: x.z)
    return items


def extract_rec(pallet: Container):
    """ Treat this method as a black box, feed pallet container receive list of items.

    :param pallet:
    :return:
    """
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
    result = spaces.copy()
    print("Entering sort_spaces...")

    # This line was not sorting the spaces, leaving it for future editing. I feel that its related to the lambda func.
    # sorted(result, key=lambda x: x.z)
    res = insertion(spaces, 0, len(spaces) - 1)
    for x in res:
        print(x.logi_coord, x.size)
    print("Exiting sort_spaces...")
    return res


def insertion(arr, left, right) -> list:
    for i in range(left + 1, right + 1):
        j = i
        while j > left and arr[j].z < arr[j - 1].z:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1
    return arr
