#!/usr/bin/python
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import argparse
import sys
import csv
from xml.sax.saxutils import unescape
from Nosh import Nosh
from NetworkError import NetworkError


def write_csv_file(filename, dictionary):
    """ Writes the dictionary as CSV to the specified file """
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        for key, value in dictionary.items():
            writer.writerow([unescape(key.encode("utf-8")),
                             unescape(value.encode("utf-8"))])


def terminal_print(string):
    """ Prints a string to STDOUT """
    sys.stdout.write(string)
    sys.stdout.flush()


def main():
    """ Reads a Nosh.com restaurant URL
    Gets items and descriptions
    Writes the output as a CSV file """
    parser = argparse.ArgumentParser(description='A parser for Nosh.com')
    parser.add_argument('url', help='Valid nosh.com URL from a restaurant')
    parser.add_argument('-o', dest='output', help='Filename for the output',
                        default=None)

    args = parser.parse_args()

    nosh = Nosh()
    terminal_print("\rGetting restaurant... ")
    try:
        menu_items = nosh.get_menu_items_from_url(args.url)
        terminal_print("DONE!\n")
        count = len(menu_items)
        i = 0
        for mi in menu_items:
            terminal_print("\rGetting items: %s / %s (%s%%)" %
                           (i, count, (100 * i / count)))
            description = nosh.get_item_description_from_url(menu_items[mi])
            menu_items[mi] = description
            i += 1

        if menu_items:
            terminal_print("\rGetting items... DONE!%s\n" % (' ' * 20))
            if not args.output:
                regex = re.compile('(\d+)')
                restaurant_id = regex.findall(args.url)[0]
                filename = '%s.csv' % restaurant_id
            else:
                filename = args.output
            terminal_print("\rItems saved in: %s\n" % filename)
            write_csv_file(filename, menu_items)
        else:
            terminal_print("\rNo items found!\n")
    except Exception, e:
        if hasattr(e, 'msg'):
            print e.msg
        else:
            print e


if __name__ == '__main__':
    main()
