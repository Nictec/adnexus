def merge(dict1: dict, dict2: dict) -> dict:
    new_dict = {}
    for key, value in dict1.items():
        new_dict[key] = value

    for key, value in dict2.items():
        new_dict[key] = value

    return new_dict
