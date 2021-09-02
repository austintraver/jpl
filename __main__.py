import json
import plistlib
from datetime import datetime
from pathlib import Path
from argparse import ArgumentParser, Namespace
from sys import stdout
from typing import IO


def default(obj):
    """
    Determine how to handle decoding timestamps from string format
    :param obj:
    :return:
    """
    if isinstance(obj, datetime):
        return {'fmt': obj.isoformat()}
    raise TypeError('...')


def object_hook(obj):
    """
    Determine how to handle encoding timestamps into string format
    :param obj:
    :return:
    """
    fmt = obj.get('fmt')
    if fmt is not None:
        return datetime.fromisoformat(fmt)
    return obj


def parse_arguments() -> Namespace:
    # Create the parser to process any command-line arguments provided as input.
    parser = ArgumentParser(
        prog='jpl',
        usage='%(prog)s IFILE [{-o|--output} OFILE]',
        description='%(prog)s: a plist conversion utility'
    )
    parser.add_argument(
        dest='ifile',
        type=str,
        metavar='IFILE',
        help='the path to the input file to read from',
    )
    parser.add_argument(
        '-o',
        '--output',
        dest='ofile',
        type=str,
        help='the path to the output file to write to'
    )
    return parser.parse_args()


def plist_to_json(ifile: IO, ofile: IO):
    """
    Re-encode a Property List file as JSON
    :param ifile: The Property List file to read the input from
    :param ofile: The JSON file to write the output to
    """
    # Read in the preferences from the .plist file.
    prefs = plistlib.load(ifile)
    # Write out the preferences in .json format.
    json.dump(prefs, ofile, default=default, indent=4)


def json_to_plist(ifile: IO, ofile: IO):
    """
    Re-encode a JSON file as a Property List
    :param ifile: The JSON file to read the input from
    :param ofile: The Property List file to write the output to
    """
    # Read in the preferences from the .json file.
    prefs = json.load(ifile, object_hook=object_hook)
    # Write out the preferences in .plist format.
    plistlib.dump(prefs, ofile)


def main():
    args = parse_arguments()

    ifile: IO = open(args.ifile, 'rb')
    ofile: IO = open(args.ofile, 'wb') if args.ofile else stdout

    # If the file is a Property List, convert its underlying contents to JSON
    if args.ifile.endswith('.plist'):
        plist_to_json(ifile, ofile)

    # If it is a JSON file, convert its underlying contents to a Property List
    elif args.ifile.endswith('.json'):
        json_to_plist(ifile, ofile)


if __name__ == '__main__':
    main()
