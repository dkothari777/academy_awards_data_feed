import json
from pathlib import Path

def write_out(module:str, filename:str, data):
    cwd = Path.cwd()
    target_path = cwd.joinpath(f"data/{module}").mkdir(parents=True, exist_ok=True)
    filename = f"data/{module}/{filename}"
    with open(filename, "w") as fs:
        json.dump(data, fs)