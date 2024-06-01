#!/usr/bin/python3

import argparse
from dateutil import parser as date_parser
from dateparser.search import search_dates
import yaml

# Create ArgumentParser object
argument_parser = argparse.ArgumentParser(description='Process edition.')

# Add positional argument
argument_parser.add_argument('edition', type=str, help='Specify the edition.')

# Parse the arguments
args = argument_parser.parse_args()

print(f"processing {args.edition}...")

with open(args.edition, "r") as edition:
    lines = edition.readlines()

with open("global_parameters.yaml", "r") as yaml_file:
   global_parameters = yaml.safe_load(yaml_file)

print()
print(f"checking announcement headers for completeness:...")
announcement_headers = [line.strip() for line in lines if line.strip().startswith(global_parameters["announcement_header"])]
for announcement_header in announcement_headers:

    index_semicolon = announcement_header.find(":")
    if( index_semicolon == -1 ):
        print(f"check format of '{announcement_header}'!")
    else:
        first_part = announcement_header[: index_semicolon]

        try:
            year = search_dates(first_part)
            if( year is None ):
                print(f"add year to '{announcement_header}'")
        except Exception as e:
            print(f"error finding year in '{announcement_header}'")
            print(str(e))
print()

