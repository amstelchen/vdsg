#!/usr/bin/env python

import argparse, time, os, sys
import textwrap

PROGNAME = "VDSG"
VERSION = "0.1.0"
DEBUG = '''>SET HALT RESTART/MAINT
RETROS BIOS
RBIOS-4.02.08.00 52EE5.E7.E8
Copyright 2201-2203 Robco Ind.
Uppermem: 64 KB
Root (5A8)
Maintenance Mode
>RUN DEBUG/OPTIONS.F'''

AUTHOR = "Copyright 2022-2077 Michael John, \nCopyright 2201-2203 RobCo Industries"
DESC = "Search the VDSG catalogue"
EPILOG="search criteria:"

def parse_data(path, file, debug=False):
    if debug:
        print(f"Fetching {file}")
    data = {}
    with open(os.path.join(path, file), mode = "rt", encoding = "utf-8") as f:
        for line in f: # .readlines():
            (n, e) = line.split("\t")
            data[int(n)] = e.strip()
    return data

def print_data(data, filter, wrap=0, debug=False):
    try:
        if isinstance(filter, str):
            result = [p for p in data if filter in data[p]]
            #print(result)
            for entry in result:
                entry_text = "\n".join(textwrap.wrap(data[entry], width=wrap)) if wrap > 0 else data[entry]
                print(f'VDSG Catalogue No.{entry}\n{entry_text}')
        if isinstance(filter, int):
            entry_text = "\n".join(textwrap.wrap(data[filter], width=wrap)) if wrap > 0 else data[filter]
            print(f'VDSG Catalogue No.{filter}\n{entry_text}')
    except KeyError:
        print(f'Entry {filter} not found.')

def main():
    start = time.time()

    parser = argparse.ArgumentParser(prog=PROGNAME, description=DESC)  #, epilog=EPILOG + criteria_str)
    parser.add_argument('-n', dest='number', help='search for specified VDSG catalogue number', type=int)
    parser.add_argument('-t', dest='text', help='search for text in VDSG catalogue', type=str)
    parser.add_argument('-l', dest='list_all', help='list all VDSG catalogue entries', action='store_true')
    parser.add_argument('-w', dest='chars', help='wrap text at CHARS characters', type=int)
    parser.add_argument('-d', '--debug', help='enable debug output', action='store_true')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + VERSION + ' ' + AUTHOR)

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    debug = vars(args)["debug"]
    if debug:
        print(DEBUG)
        print(str(args).replace("Namespace", "Options"))

    data = parse_data(os.path.dirname(__file__), "Catalogue.F", debug)

    chars = 0
    if vars(args)["chars"] is not None and int(vars(args)["chars"]) > 0:
        chars = vars(args)["chars"]

    list_all = vars(args)["list_all"]
    if list_all:
        #print(data)
        for entry in data:
            entry_text = "\n".join(textwrap.wrap(data[entry], width=chars, subsequent_indent=" ".ljust(len(str(entry)) + 2))) if chars > 0 else data[entry]
            print(f'{entry}: {entry_text}')
        exit(0)

    if vars(args)["number"] is not None and int(vars(args)["number"]) > 0:
        filter = vars(args)["number"]
        print_data(data, filter=filter, wrap=chars, debug=debug)

    if vars(args)["text"] is not None and len(vars(args)["text"]) > 0:
        filter = vars(args)["text"]
        print_data(data, filter=filter, wrap=chars, debug=debug)

    end = time.time()
    if debug:
        print('[{:2.3} seconds elapsed]'.format((end - start)))
