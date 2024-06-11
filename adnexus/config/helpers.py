def merge(dict1: dict, dict2: dict) -> dict:
    """
    helper function to merge multiple config sources
    :param dict1: first dict to merge
    :param dict2: second dict to merge
    :return: merged dict
    """
    new_dict = {}
    for key, value in dict1.items():
        new_dict[key] = value

    for key, value in dict2.items():
        new_dict[key] = value

    return new_dict
