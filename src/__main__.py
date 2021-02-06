import argparse
import GUI


class Namespace:
    nogui = False


def main():
    c = Namespace()
    parser = argparse.ArgumentParser(allow_abbrev=False)
    # Arguments declared here
    parser.add_argument("--nogui", action="store_true", help="Will not start the GUI")
    parser.parse_args(namespace=c)
    if not c.nogui:
        # Start GUI
        GUI.start()
    print('Hello world!')


if __name__ == '__main__':
    main()
