import json

def JsonGetInfo(path: str) -> dict:
    with open(path, 'r') as File:
        Content = json.load(File)
        File.close()
    return Content

def JsonSaveInfo(Info, path: str):
    with open(path, 'w') as File:
        json.dump(Info, File, indent=4)
        File.close()