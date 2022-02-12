import os

API_KEY_NAME = "x-api-key-name"


def get_config() -> dict:
    config: dict = {}
    for k, v in os.environ.items():
        if k.startswith("KEY_"):
            env = v.split("|")
            config[k.lower()] = dict(
                part=env[0],
                key=env[1],
                value=env[2],
            )
    return config


config = get_config()
