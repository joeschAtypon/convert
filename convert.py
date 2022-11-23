import argparse
import toml
import json
import yaml
import os

#######################
# setup our arguments
#######################

parser = argparse.ArgumentParser(
    description="Converts between json, yaml, and toml file formats")
parser.add_argument("file", help="input filename",
                    type=argparse.FileType('r', encoding='UTF-8'))
parser.add_argument("--out", help="the output file format",
                    choices=["yaml", "json", "toml"])
parser.add_argument(
    "--in", help="input file format. If not provided, the script tries to auto detect format from filename", choices=["yaml", "json", "toml"])
parser.add_argument(
    "-o", "--output-file", help="the output filename. If not provided, the output file will have the same name as the input file")
parser.add_argument(
    "-p", "--print", help="print converted file contents to console instead of writing to output file", action="store_true")
args = parser.parse_args()

########################

# split the input file into the filename and extension
# this can be used if the optional arguments aren't passed
filename, file_extension = os.path.splitext(args.file.name)

with open(args.file.name) as f:
    if file_extension.strip('.') == 'yaml':
        data = yaml.load(f, Loader=yaml.SafeLoader)
    elif file_extension.strip('.') == 'json':
        data = json.loads(f.read())
    elif file_extension.strip('.') == 'toml':
        data = toml.loads(f.read())

if args.print:
    if args.out == 'yaml':
        print(yaml.dump(data))
    elif args.out == 'json':
        print(json.dumps(data, indent=4, sort_keys=True, default=str))
    elif args.out == 'toml':
        print(toml.dumps(data))
else:
    # set output file format
    if args.out:
        file_extension = args.out

    # set output filename
    if args.output_file:
        filename = args.output_file

    with open(filename+'.'+file_extension, "w") as f:
        if args.out == 'yaml':
            f.write(yaml.dump(data))
        elif args.out == 'json':
            f.write(json.dumps(data, indent=4, sort_keys=True, default=str))
        elif args.out == 'toml':
            f.write(toml.dumps(data))
