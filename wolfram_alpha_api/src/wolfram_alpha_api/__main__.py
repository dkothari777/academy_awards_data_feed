import os
import requests
import json

WOLFRAM_APP_ID=os.environ["WOLFRAM_APP_ID"]
WOLFRAM_API_URL="https://api.wolframalpha.com/v2/query"

def write_out(year: int, data):
    filename = f"AcademyAwards{year}.json"
    with open(filename, "w") as fs:
        json.dump(data, fs)

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
    write_out(year, result["subpods"])

if __name__ == '__main__':
    main()