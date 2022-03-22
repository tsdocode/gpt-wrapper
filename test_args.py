# Include standard modules
import argparse

# Initiate the parser
parser = argparse.ArgumentParser()

parser.add_argument("-V", "--version", help="show program version", action="store_true")
args = parser.parse_args()

if args.version:
    print("This is myprogram version 0.1")
    