from argparse import ArgumentParser
from pathlib import Path
import json
from common.util import write_out, get_year


def get_title(to_parse: str):
    index = to_parse.find(" (")
    if index != -1:
        title = to_parse.split(" (")[0].strip()
        produced_by = to_parse.split(" (")[1].removesuffix(")").strip()
        return (title, produced_by)
    else:
        return None

def get_actor(to_parse: str):
    index = to_parse.find(" in ")
    if index != -1:
        title = to_parse.split(" in ")[1].strip()
        actor = to_parse.split(" in ")[0].strip()
        return (title, actor)
    else:
        return None
    
def get_other(to_parse: str):
    index = to_parse.find(" for ")
    if index != -1:
        title = to_parse.split(" for ")[1].strip()
        talent = to_parse.split(" for ")[0].strip()
        return (title, talent)
    else:
        return None


def extrapolate(row, year):
    row["year"] = year
    to_parse = row["winner"].strip()
    tuple_title = get_title(to_parse)
    if tuple_title:
        row["title"] = tuple_title[0]
        row["produced_by"] = tuple_title[1]
    else:
        tuple_title = get_actor(to_parse)
        if tuple_title:
            row["title"] = tuple_title[0]
            row["actor"] = tuple_title[1]
        else:
            tuple_title = get_other(to_parse)
            if tuple_title:
                row["title"] = tuple_title[0]
                row["talent"] = tuple_title[1]
            else:
                row["title"] = None
                row["data_note"] = "Not parsed"
    return row

def parse_data(filename, data):
    year = get_year(filename)
    results = [extrapolate(row, year) for row in data]
    return results

def main():
    argparser = ArgumentParser(prog="extrapolate", description="extracts award winners/nominees from wolframalpha json")
    argparser.add_argument("-d", "--data-dir")
    args = argparser.parse_args()
    data_dir = args.data_dir
    filepaths = list(Path(data_dir).glob("*.json"))
    for file in filepaths:
        with open(file, "r") as fs:
            json_str = fs.read()
        data = json.loads(json_str)
        parsed_results = parse_data(file.name,data)
        write_out("extrapolate", file.name.split("/")[-1], parsed_results)


if __name__ == '__main__':
    main()