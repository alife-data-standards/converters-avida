"""
avida-to-standard-phylogeny.py

This script converts an avida .spop file into ALife standard-compliant phylogeny
file.

Currently outputs in format assumed by pandas.

Currently outputs each entry in output file in order they were read in from Avida
file.

Currently assumes Avida defaults in .spop fields.
"""

import argparse, os, copy
import pandas as pd

VALID_OUT_FORMATS = ["csv", "json"]
AVIDA_SET_FIELDS = ["parents", "cells", "gest_offset", "lineage"]
AVIDA_SET_DELIM = ","

def Convert_AvidaSpop_To_StdPhylogeny(input_fpath, output_fpath=None, output_format="csv", minimal_output=False):
    """Convert Avida .spop file (default population output file for Avida) to ALife
       standard phylogeny format.

    Args:
        input_fpath (str): The path to the target Avida .spop file.
        output_fpath (str): The full path (including file name) to write standard
            phylogeny file to. If set to 'None', will output in same location as
            the specified Avida .spop file.
        output_format (str): The output format. Must be one of a valid set of supported
            output formats ('CSV', 'JSON')
        minimal_output (boolean): Should output be minimal? If so, only output minimal
            requirements (+ available conventional fields) for phylogeny standard.
    
    Returns:
        bool: True if successful, False otherwise.
    
    Raises:
        ValueError: If input_fpath is invalid.
        ValueError: If output_format does not specify a supported format.
        ValueError: If Avida IDs are not unique in the given input file.

    """
    # Is input_fpath a valid file?
    if (not os.path.isfile(input_fpath)):
        raise ValueError("Failed to find provided input file ({})".format(input_fpath))

    # Is output_format valid?
    if (not output_format in VALID_OUT_FORMATS):
        raise ValueError("Invalid output format provided ({}). Valid arguments include: {}".format(output_format, VALID_OUT_FORMATS))
    
    output_fpath = output_fpath if (output_fpath != None) else input_fpath.replace(".spop", "_standard-phylogeny.{}".format(output_format))

    # Open and parse input file into pandas data frame.
    # - Read in file, store as dict, use dict to make pandas dataframe object.
    with open(input_fpath, "r") as fp:
        # Extract header information.
        header = None
        for line in fp:
            if line[:7] == "#format":
                header = line.replace("#format", "").strip().split(" ")
                break
        if header == None:
            exit("Failed to find file format information in {}".format(input_fpath))
        
        # Collect data from Avida file in format that will be easy to convert to
        # pandas dataframe object.
        avida_data = {field:[] for field in header}
        for line in fp:
            line = line.strip()
            # Consume all comment lines and blank lines.
            if line == "" or line[0] == "#": continue
            # If we're here, we're looking at data.
            # Note, Avida's output is pretty disgusting. We can't assume that all
            # trailing fields will exist on a line. :barf:
            line = line.split(" ")
            for i in range(0, len(header)):
                # If we don't have the value for a field, set to 'NONE'
                value = line[i] if i < len(line) else "NONE"
                # If the field is known to be a set, split on ','
                if header[i] in AVIDA_SET_FIELDS: value = value.split(AVIDA_SET_DELIM)
                # Go ahead and add the value to the appropriate field.
                avida_data[header[i]].append(value)

    # Clean up avida data to play with standard.
    avida_data["ancestor_list"] = [list(map(int, [-1 if anc == "(none)" else anc for anc in anc_lst])) for anc_lst in avida_data.pop("parents")]
    avida_data["origin_time"] = copy.deepcopy(avida_data["update_born"])
    avida_data["id"] = list(map(int, avida_data["id"]))

    # Are all IDs unique?
    id_set = set(avida_data["id"])
    if (len(avida_data["id"]) != len(id_set)):
        raise ValueError("Avida organism IDs must be unique!")
    
    # Convert Avida data into pandas data frame.
    df = pd.DataFrame(data = avida_data)

    # Drop any fields we want to delete.
    del_fields = []
    if minimal_output:
        # What fields should we delete (if we're doing minimal output)?
        min_fields = ["id", "ancestor_list", "origin_time"]
        del_fields = [field for field in avida_data if not field in min_fields]
        df.drop(del_fields, axis=1, inplace=True)

    # Adjust the header so that standard fields are up front.
    stds_hd = ["id", "ancestor_list", "origin_time"]
    new_header = stds_hd + [field for field in avida_data if (not field in stds_hd) and (not field in del_fields)]
    # Write output in requested format.

    # print(len(df.id.unique()))
    df.set_index("id", inplace=True, drop=False)

    if (output_format == "csv"):
        with open(output_fpath, "w"):
            df.to_csv(output_fpath, sep=",", columns=new_header, index=False, index_label=False)
    elif (output_format == "json"):
        with open(output_fpath, "w"):
            df.to_json(output_fpath, orient="index")

    return True

def main():
    # Setup command line arguments.
    parser = argparse.ArgumentParser(description="Avida .spop to ALife standard-compliant phylogeny converter.")
    parser.add_argument("input", type=str, help="Input avida .spop file.")
    parser.add_argument("-output", "-out", type=str, help="Name to assign to standard-compliant output file.")
    parser.add_argument("-format", type=str, default="csv", help="What standard file format should this script output? Valid options: {}".format(VALID_OUT_FORMATS))
    parser.add_argument("-minimal", action="store_true", help="Store minimal data in output file.")
    parser.add_argument("-list_formats", "-lsf", action="store_true", help="List available output formats.")

    # Parse command line arguments.
    args = parser.parse_args()

    if (args.list_formats):
        print("Valid output formats include: {}".format(VALID_OUT_FORMATS))
        print("File an issue here to request new formats: https://github.com/alife-data-standards/converters-avida/issues")
        return

    # Extract/validate arguments
    in_fp = args.input
    out_fp = args.output
    out_format = args.format.lower()
    minimal_out = args.minimal

    print("Converting {}".format(in_fp))
    if (Convert_AvidaSpop_To_StdPhylogeny(in_fp, out_fp, out_format, minimal_out)):
        print("Success!")
    else:
        print("Ah! Something went wrong.")

if __name__ == "__main__":
    main()