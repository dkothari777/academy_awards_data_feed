import os
import aiohttp.client_reqrep
import requests
from datetime import datetime
import asyncio
import aiohttp
from common.util import write_out, list_files, get_year
import time
from pathlib import Path

WOLFRAM_APP_ID=os.environ["WOLFRAM_APP_ID"]
WOLFRAM_API_URL="https://api.wolframalpha.com/v2/query"
ACADEMY_AWARDS_START_YEAR=1929 #1929 year that awards started
QUEUE: list[int] = []

async def get_academy_awards(year:int):
    print(f"Capturing Academy Awards Year: {year}")
    input=f"Academy Awards Nominees {year}"
    count = 2
    params = {"input": input, "output": "json", "appid": WOLFRAM_APP_ID}
    has_more = True
    json_response = None
    while(has_more):
        try:
            params["podstate"] = f"{count}@Result__More"
            async with aiohttp.ClientSession() as session:
                async with session.get(WOLFRAM_API_URL, params=params) as response:
                    json_response = await response.json()
            result = json_response["queryresult"]["pods"][1]
            has_more = False
            states = result["states"]
            for state in states:
                if state["name"].lower() == "more": 
                    print(f"There is more to capture. Current count {count}. Incrementing...")
                    count +=1
                    has_more = True
        except Exception as e:
            # print(json_response)
            print(e)
            return False
    write_out("retrieve", f"AcademyAwards{year}.json", json_response)
    print(f"Finish collecting Academy awards for {year}.")
    return True

async def semwrapper(task: int, sem: asyncio.Semaphore) -> bool:
    async with sem:
        result = await get_academy_awards(task)
        return result

def generate_queue(start_year:int, end_year:int) -> list[int]:
    queue: list[int] = []
    files: list[Path] = list_files("retrieve")
    years_persisted: list[int] = []
    for file in files:
        year = get_year(file.name)
        years_persisted.append(year)
    for year in range(start_year, end_year):
        if year not in years_persisted:
            queue.append(year)
    return queue

async def main():
    current_year = datetime.now().year + 1
    sem = asyncio.Semaphore(10)
    queue: list[int] = generate_queue(ACADEMY_AWARDS_START_YEAR, current_year)
    async_tasks = [semwrapper(year, sem) for year in queue]
    await asyncio.gather(*async_tasks)

if __name__ == '__main__':
    asyncio.run(main())