import argparse
import json


parser = argparse.ArgumentParser()
parser.add_argument("--payload-file", type=argparse.FileType("r"))
parser.add_argument("--output", type=argparse.FileType("w"))
args = parser.parse_args()

payload = json.load(args.payload_file)
for row in payload["entries"]:
    key = row["key"]
    value = row["text_value"]
    var = f"{key}={value}\n"
    args.output.write(var)