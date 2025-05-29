import os
import requests
import json

WOLFRAM_APP_ID=os.environ["WOLFRAM_APP_ID"]
WOLFRAM_API_URL="https://api.wolframalpha.com/v2/query"

def write_out(year: int, data):
    filename = f"AcademyAwards{year}.json"
    with open(filename, "w") as fs:
        json.dump(data, fs)

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
    year=2025
    input=f"Academy Awards Nominees {year}"
    output="json"
    params = {"input": input, "output": "json", "appid": WOLFRAM_APP_ID, "podstate": "Result__More"}
    count = 1
    has_more = True
    while(has_more):
        try:
            if count == 1:
                response = requests.get(WOLFRAM_API_URL, params=params)
            else:
                params["podstate"] = f"{count+1}@Result__More"
                response = requests.get(WOLFRAM_API_URL, params=params)
            result = response.json()["queryresult"]["pods"][1]
            has_more = False
            states = result["states"]
            for state in states:
                if state["name"].lower() == "more": 
                    print(f"There is more to capture. Current count {count}. Incrementing...")
                    count +=1
                    has_more = True
        except Exception as e:
            print(e)
            break
    parsed_results = parse_subpods(result["subpods"])
    write_out(year, parsed_results)

if __name__ == '__main__':
    main()