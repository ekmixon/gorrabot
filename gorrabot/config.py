import yaml
from api.vault import SECRET_NAME, get_secret


def read_config() -> dict:
    try:
        return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit(1)


config = read_config()
