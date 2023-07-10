#! /usr/bin/env python3
import csv
import json
import argparse


# Columns common to all courses
COMMON_COLUMNS = {"id"}


def main():
    parser = argparse.ArgumentParser(
        prog="csv2json", description="Convert a course csv to data and topics json"
    )
    parser.add_argument("part", help="IA, IB, II, etc.")
    parser.add_argument("course", help="Full course name")
    parser.add_argument("infile", help="input csv")
    parser.add_argument(
        "outfile_prefix",
        help="prefix of output data and topics files, usually lowercase course name with ' ' -> '_'",
    )
    args = parser.parse_args()

    outdatafile = f"{args.outfile_prefix}.data.json"
    outtopicsfile = f"{args.outfile_prefix}.topics.json"

    with open(args.infile) as f:
        reader = csv.DictReader(f)

        # Make topics list
        # Using list comprehension instead of set subtraction to retain order
        topics = [x for x in reader.fieldnames if x not in COMMON_COLUMNS]
        with open(outtopicsfile, "w") as f:
            f.write(json.dumps(topics, indent=4))

        # Construct output data
        data = []

        for inrow in reader:
            outrecord = {}

            # Copy common columns over
            for col in COMMON_COLUMNS:
                outrecord[col] = inrow[col]

            # Add data not in sheet
            outrecord["id"] = "_".join([args.part, outrecord["id"]])
            outrecord["course"] = args.course

            # Populate topic columns
            outrecord["topics"] = []
            for col in inrow.keys() - COMMON_COLUMNS:
                value = inrow[col]
                if value:
                    outrecord["topics"].append(col)

            # print(outrecord)
            data.append(outrecord)

        with open(outdatafile, "w") as f:
            f.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
