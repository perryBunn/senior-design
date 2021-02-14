import argparse
import GUI
import Ingest
import logging
import pandas as pd
from lib import Item
import Sort


def init(data) -> list:
    items = []
    for item in data.iterrows():
        obj = Item.Item(item[1]["Length"], item[1]["Width"], item[1]["Height"], item[1]["Weight"], item[1]["Code/Serial Number"])
        items.append(obj)
    return items


class Namespace:
    nogui = False
    ingest = []


def main():
    logging.basicConfig(filename='../logs/debug.log', level=logging.DEBUG, encoding='utf-8',
                        format='%(asctime)s %(levelname)s: %(message)s')
    logging.debug("Debug")
    logging.info("Info")
    logging.warning("Warning")
    logging.error("Error")
    logging.critical("Critical")
    logging.info("Logger successfully created")
    c = Namespace()
    parser = argparse.ArgumentParser(allow_abbrev=False)
    # Arguments declared here
    parser.add_argument("--ingest", nargs=1, help="Ingest a file for packing")
    parser.add_argument("--nogui", action="store_true", help="Will not start the GUI")
    parser.parse_args(namespace=c)
    logging.debug('Hello world!')
    if not c.nogui:
        # Start GUI
        logging.debug("Starting GUI...")
        GUI.start()
    else:
        logging.debug("GUI not started...")
    if len(c.ingest) > 0:
        data = Ingest.ingest("../", c.ingest[0])
        items = init(data)
        items = Sort.item_sort(items)
        print(items[0])
        print(items[len(items)-1])


if __name__ == '__main__':
    main()
