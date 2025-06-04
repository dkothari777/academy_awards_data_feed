from pathlib import Path
from argparse import ArgumentParser
from common.util import write_out
from pathlib import Path
import json

def parse_subpods(data):
    results = []
    for x in data:
        award = x["title"]
        winners_nominees = x["plaintext"].split("\n")
        for nominated in winners_nominees:
            award_type = "winner" if nominated.split("|")[0].strip() == "winner" else "nominated"  # winner | nominee
            winner = nominated.split("|")[1].strip()
            results.append({"award": award, "award_type": award_type, "winner": winner})
    return results

def main():
    argparser = ArgumentParser(prog="extract", description="extracts award winners/nominees from wolframalpha json")
    argparser.add_argument("-d", "--data-dir")
    args = argparser.parse_args()
    data_dir = args.data_dir
    filepaths = list(Path(data_dir).glob("*.json"))
    for file in filepaths:
        with open(file, "r") as fs:
            json_str = fs.read()
        data = json.loads(json_str)
        subpods = data["queryresult"]["pods"][1]["subpods"]
        parsed_results = parse_subpods(subpods)
        write_out("extract", file.name.split("/")[-1], parsed_results)


if __name__ == '__main__':
    main()