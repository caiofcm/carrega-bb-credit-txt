# from __future__ import print_function, absolute_import

import argparse
from parse_bb_credit import print_expenses

description = """
Parse BB Credit Cards .TXT file
"""


def main():
    ap = argparse.ArgumentParser(description=description)
    ap.add_argument("source", help="Arquivo txt com a fatura")
    # ap.add_argument("destination", help="output notebook filename")
    args = ap.parse_args()
    # Process
    print_expenses(args.source)


if __name__ == '__main__':
    main()
