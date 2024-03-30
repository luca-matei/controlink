"""
Check if config.json exists. If not, create a copy of config.default.json and save it as config.json.
Load config.json into a pydantic settings model.
"""

import orjson
from pydantic import BaseModel

with open("config.json", "r") as f:
    config_json = f.read()
    config_json = orjson.loads(config_json)


class ServerSettings(BaseModel):
    host: str
    port: int


class ClientSettings(BaseModel):
    server_host: str
    server_port: int


class Settings(BaseModel):
    server: ServerSettings
    client: ClientSettings


settings = Settings(**config_json)
