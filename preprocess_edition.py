#!/usr/bin/python3

import argparse
from dateutil import parser as date_parser
from dateparser.search import search_dates
import os
import pandas
import string
import yaml

# this is abuse
class Deadline:

    def __init__(self, announcement=None, description=None, date=None):
        self.announcement = announcement
        self.description = description
        self.date = date

    def __repr__(self):

        return f"{self.announcement:<50}\t{self.description:<40}\t{str(self.date):<30}"

# Create ArgumentParser object
argument_parser = argparse.ArgumentParser(description='Process edition.')

# Add positional argument
argument_parser.add_argument('edition', type=str, help='Specify the edition.')

# Parse the arguments
args = argument_parser.parse_args()

print(f"processing {args.edition}...")

#output_filename = args.edition + "preprocessed.md"
output_filename = os.path.splitext(args.edition)[0] + "_preprocessed.md"

with open(args.edition, "r") as edition:
    lines = edition.readlines()
    original_lines = edition.readlines()

with open("global_parameters.yaml", "r") as yaml_file:
   global_parameters = yaml.safe_load(yaml_file)

print()
print(f"checking announcement headers for completeness:...")
announcement_headers = [line.strip() for line in lines if line.strip().startswith(global_parameters["announcement_header"])]
for announcement_header in announcement_headers:

    # split the line at the NECESSARY semicolon
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

print(f"formatting dates and deadlines...")
for i in range(len(lines)):

    line = lines[i]

    # check for date flags
    # -dv is not checked because we leave it verbatim, as the flag suggests (e.g. for date ranges)
    if( line.strip().startswith(
       (global_parameters["date_flag"],
        global_parameters["edition_date_flag"],
        global_parameters["previous_edition_date_flag"],
        global_parameters["deadline_flag"] )) ):

        # split the line at the NECESSARY semicolon
        if( line.find(":") != -1 ):

            # the date is the last part of the string (unless you did it wrong)
            date_part = line.strip().split(":")[-1]

            # find the date itself, then replace it with its formatted version
            results = search_dates(date_part)
            for result in results:  # the result comes in a list of tuples, so we have to iterate
                formatted_date = result[1].strftime(global_parameters["date_format"])
                lines[i] = line.replace(result[0], formatted_date)

        # complain if the NECESSARY semicolon is not there
        else:
            print(f"*** no semicolon in date format: {line}")



# construct per-announcement table of important dates
# all dates must be in a single, contiguous region
date_flags = [global_parameters["date_flag"],
        global_parameters["edition_date_flag"],
        global_parameters["deadline_flag"],
        global_parameters["verbatim_date_flag"]]

deadline_columns = ["announcement", "description", "date"]
deadlines = pandas.DataFrame(columns=deadline_columns)
contiguous_region = False
current_announcement = None
for i in range(len(lines)):

    line = lines[i]

    if( line.strip().startswith( global_parameters["announcement_header"] ) ):
        line_split = lines[i].strip().split(":")
        current_announcement = line_split[0].replace(global_parameters["announcement_header"], "").strip()

    if( line.strip().startswith( tuple(date_flags) ) ):
        
        line_split = lines[i].strip().split(":")

        if( not contiguous_region ):

            contiguous_region = True

            # put header
            lines[i] = "\n| Important Dates | |\n|---|---|\n" + " | " + line_split[0]  + " | " + line_split[1] + " |\n"

        else:
            # put row
            lines[i] = " | " + line_split[0]  + " | " + line_split[1] + " |\n"

        for date_flag in date_flags:
            lines[i] = lines[i].replace(date_flag, "")

        if( line.strip().startswith( global_parameters["deadline_flag"] ) ):
            line = line.replace( global_parameters["deadline_flag"], "" ).strip(string.whitespace)

            date = search_dates(line)[-1][-1]

            deadlines.loc[len(deadlines)] = dict(zip(deadline_columns, [current_announcement, line, date]))
            #deadlines.append( dict(zip(deadline_columns, [current_announcement, line, date])) )

    else:
        contiguous_region = False

    if( line.strip().startswith( global_parameters["previous_edition_date_flag"] ) ):

        line_split = line.replace( global_parameters["previous_edition_date_flag"], "" ).split(":")

        date = search_dates(line_split[1])[-1][-1]


        deadlines.loc[len(deadlines)] = dict(zip(deadline_columns, [line_split[0].strip(string.whitespace), line_split[1].strip(string.whitespace), date] ))
        #deadlines.append( dict(zip(deadline_columns, [line_split[0].strip(string.whitespace), line_split[1].strip(string.whitespace), date] )) )

        lines[i] = ""

deadlines = deadlines.sort_values(by="date")
aggregated_deadlines = deadlines.groupby("announcement").agg({"description": lambda x: "; ".join(x), "date": "min"}).sort_values(by="date").reset_index()

#print()
#print("found the following deadlines:")
#print(deadlines)
#print(aggregated_deadlines)
##for deadline in deadlines:
##    print(deadline)

aggregated_deadlines = aggregated_deadlines.drop(columns=["date"])
aggregated_deadlines = aggregated_deadlines.rename(columns={"announcement":"Event", "description":"Deadlines"})

print( aggregated_deadlines.to_markdown(index=False) )

# construct table of contents
toc_entry_columns = ["name", "display_name", "type"]
toc_entries = pandas.DataFrame(columns=toc_entry_columns)
current_announcement = None
current_display_name = None
for line in lines:
    if( line.strip().startswith( global_parameters["announcement_header"] ) ):

        current_announcement = line.strip()
        line_split = line.strip().split(":")
        current_display_name = line_split[0].replace( global_parameters["announcement_header"], "" ).strip()

    elif( line.strip().startswith( global_parameters["announcement_type"] ) ):
        current_type = line.replace( global_parameters["announcement_type"], "" ).strip()
        toc_entries.loc[len(toc_entries)] = dict(zip( toc_entry_columns, [current_announcement, current_display_name, current_type] ))
        

#announcement_headers = [line.strip() for line in lines if line.strip().startswith(global_parameters["announcement_header"])]
#type_headers = [line.strip() for line in lines if line.strip().startswith(global_parameters["announcement_type"])]
#for i in range(len(announcement_headers)):
#    display_name = announcement_headers[i].split(":")[0]
#    toc_entries.loc[len(toc_entries)] = dict(zip( toc_entry_columns, [announcement_headers[i], display_name, type_headers[i]] ))

print("table of contents:")
print(toc_entries)

# get rid of empty lines
lines = [line for line in lines if line]

with open(output_filename, "w") as output_file:

    print(f"writing output to {output_filename}...")

    output_file.write( aggregated_deadlines.to_markdown(index=False) )
    output_file.write("".join(lines))
