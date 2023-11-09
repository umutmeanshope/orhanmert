import json


def update_dump_folder(folder: str) -> None:

    try:
        with open("config.json", "r") as file:
            config = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        config = {}

    config["dump_folder"] = folder

    with open("config.json", "w") as file:
        json.dump(config, file)


def get_dump_folder() -> str:

    with open("config.json", "r") as file:
        config = json.load(file)

    return config["dump_folder"]


def dump_folder_set():
    if get_dump_folder() is None:
        return False
    else:
        return True




