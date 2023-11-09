import json


def update_dump_folder(folder: str) -> None:
    """
    Update the config.json with the given folder path

    :param folder: Folder path
    :return: None
    """

    try:
        with open("config.json", "r") as file:
            config = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        config = {}

    config["dump_folder"] = folder

    with open("config.json", "w") as file:
        json.dump(config, file)


def get_dump_folder() -> str:
    """
    Read the config.json file to get the saved folder path

    :return: Folder path
    """

    with open("config.json", "r") as file:
        config = json.load(file)

    return config["dump_folder"]



