import json
from pathlib import Path

def write_out(module:str, filename:str, data):
    cwd = Path.cwd()
    cwd.joinpath(f"data/{module}").mkdir(parents=True, exist_ok=True)
    filename = f"data/{module}/{filename}"
    with open(filename, "w") as fs:
        json.dump(data, fs)

def list_files(module: str) -> list[Path]:
    cwd = Path.cwd()
    cwd.joinpath().mkdir(parents=True, exist_ok=True)
    return list(cwd.joinpath(f"data/{module}").glob("*.json"))