import yaml
import re
from functools import lru_cache

from gorrabot.api.vault import SECRET_NAME, GORRABOT_CONFIG_FILE, get_secret


def load_yaml(data):
    try:
        return yaml.safe_load(data)
    except yaml.YAMLError as exc:
        print(exc)
        exit(1)


@lru_cache
def read_config(secret) -> dict:
    if not secret:
        print("Invalid secret: Be sure you've set either SECRET_NAME or GORRABOT_CONFIG_FILE")
        exit(1)

    if re.match(GORRABOT_CONFIG_FILE['path_regex'], secret):  # must be an absolute path
        if not secret.endswith('.yaml'):
            print("Invalid GORRABOT_CONFIG_FILE: It must be a .yaml file")
            exit(1)

        try:
            with open(secret, 'r') as stream:
                return load_yaml(stream)
        except FileNotFoundError:
            print("File not found")
            exit(1)

    return load_yaml(secret)


secret = get_secret(SECRET_NAME) if SECRET_NAME else GORRABOT_CONFIG_FILE['path']
config = read_config(secret)
