import argparse
import os
import datetime as dt

import Ingest
import logging
import pandas as pd

from interface import menu, interactive
from lib import Item, Container
import Sort
import palletize
import time


def init(data) -> list:
    items = []
    for item in data.iterrows():
        obj = Item.Item(item[1]["Length"], item[1]["Width"], item[1]["Height"], item[1]["Weight"],
                        item[1]["Code/Serial Number"])
        items.append(obj)
    return items


def clean_logs():
    location = '../logs/'
    date_time_format = '%Y-%m-%d_%H-%M,%S'
    files = os.listdir(location)
    files.sort(key=lambda x: dt.datetime.strptime(x[:-10], date_time_format).timestamp())
    if len(files) > 10:
        for i in range(len(files) - 10):
            path = os.path.join(location, files[i])
            if os.path.exists(path):
                os.remove(path)


class Namespace:
    nogui = False
    ingest = []


def main():
    clean_logs()
    time_str = time.strftime("%Y-%m-%d_%H-%M,%S")
    logging.basicConfig(filename=f'../logs/{time_str}_debug.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s')
    logging.captureWarnings(True)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)
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
        # menu.start()
        interactive.start()
    else:
        logging.debug("GUI not started...")
        if len(c.ingest) > 0:
            data = Ingest.ingest("../", c.ingest[0])
            items = init(data)
            items = Sort.item_sort(items)
            container = Container.Container(0, 0, 0, 1087, 1277, 980)
            shipment = palletize.palletize(items, container)
            for pallet in shipment:
                print("Pallet: ")
                for i in pallet:
                    print(i.x, i.y, i.z, i.item)


if __name__ == '__main__':
    main()
