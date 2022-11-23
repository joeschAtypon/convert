import argparse
import toml
import json
import yaml
import os
import logging

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
parser.add_argument(
    "--log-level", help="set the logging level, default is info", choices=["info", "debug", "warn", "error"], default="info")
args = parser.parse_args()

########################


def convert():
    # split the input file into the filename and extension
    # this can be used if the optional arguments aren't passed
    filename, file_extension = os.path.splitext(args.file.name)
    logging.info("Converting data")
    try:
        with open(args.file.name) as f:
            if file_extension.strip('.') == 'yaml':
                logging.info("Readining YAML data")
                data = yaml.load(f, Loader=yaml.SafeLoader)
            elif file_extension.strip('.') == 'json':
                logging.info("Reading JSON data")
                data = json.loads(f.read())
            elif file_extension.strip('.') == 'toml':
                logging.info("Reading TOML data")
                data = toml.loads(f.read())
    except Exception as e:
        logging.error("Exception occurred reading input", exc_info=True)

    try:
        if args.print:
            if args.out == 'yaml':
                logging.info("Printing YAML data")
                print(yaml.dump(data))
            elif args.out == 'json':
                logging.info("Printing JSON data")
                print(json.dumps(data, indent=4, sort_keys=True, default=str))
            elif args.out == 'toml':
                logging.info("Printing TOML data")
                print(toml.dumps(data))
        else:
            # set output file format
            if args.out:
                file_extension = args.out
            # set output filename
            if args.output_file:
                filename = args.output_file
            try:
                with open(filename+'.'+file_extension, "w") as f:
                    if args.out == 'yaml':
                        logging.info("Writing YAML data")
                        f.write(yaml.dump(data))
                    elif args.out == 'json':
                        logging.info("Writing JSON data")
                        f.write(json.dumps(data, indent=4,
                                sort_keys=True, default=str))
                    elif args.out == 'toml':
                        logging.info("Writing TOML data")
                        f.write(toml.dumps(data))
            except Exception as e:
                logging.error(
                    "Exception occurred exporting data to file", exc_info=True)
    except Exception as e:
        logging.error("Exception occurred outputting data", exc_info=True)


def main():
    numeric_level = args.log_level.upper()
    logging.basicConfig(level=numeric_level,
                        format='%(asctime)s:%(levelname)s:%(message)s', filename='convert.log')
    logging.info('Started')
    convert()
    logging.info('Finished')


if __name__ == '__main__':
    main()
