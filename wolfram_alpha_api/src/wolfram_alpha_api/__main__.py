import os
import requests

WOLFRAM_APP_ID=os.environ["WOLFRAM_APP_ID"]
WOLFRAM_API_URL="https://api.wolframalpha.com/v2/query"

def main():
    year=2025
    input=f"Academy Awards Nominees {year}"
    output="json"
    params = {"input": input, "output": "json", "appid": WOLFRAM_APP_ID}
    response = requests.get(WOLFRAM_API_URL, params=params)
    print(response.text)

if __name__ == '__main__':
    main()