"""
    Credential Loader (with fallback support)
    Class template manually created, most code was ChatGPT generated
"""

import json
import os
from configparser import ConfigParser
from jproperties import Properties
from dataclasses import dataclass
from typing import Any, Optional
from jsonpath_ng import parse


@dataclass
class Credentials:
    username: Optional[str]
    password: Optional[str]


@dataclass
class Configuration:
    host: Optional[str]
    port: Optional[int]
    database: Optional[str]
    credentials: Optional[Credentials] = None

    @property
    def connection_string(self) -> Optional[str]:
        if self.host and self.port and self.database:
            return f"{self.host}:{self.port}/{self.database}"
        return None


@dataclass
class JsonPropertyPaths:
    username: str = "credentials.username"
    password: str = "credentials.password"
    database: str = "database.name"
    host: str = "database.host"
    port: str = "database.port"


@dataclass
class IniPropertyPaths:
    section: str = "database"
    username: str = "username"
    password: str = "password"
    database: str = "name"
    host: str = "host"
    port: str = "port"


@dataclass
class PropertiesFilePropertyPaths:
    username: str = "username"
    password: str = "password"
    database: str = "database"
    host: str = "host"
    port: str = "port"


@dataclass
class EnvironmentVariables:
    username: str = "DB_USERNAME"
    password: str = "DB_PASSWORD"
    database: str = "DB_NAME"
    host: str = "DB_HOST"
    port: str = "DB_PORT"


class ConfigLoader:

    @staticmethod
    def from_json_file(file_path: str, property_paths: JsonPropertyPaths = JsonPropertyPaths()) -> Configuration:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return ConfigLoader.from_json(data, property_paths)

    @staticmethod
    def from_json(data: dict, property_paths: JsonPropertyPaths = JsonPropertyPaths()) -> Configuration:
        def extract(path: str) -> Optional[Any]:
            try:
                expr = parse(path)
                matches = expr.find(data)
                return matches[0].value if matches else None
            except Exception:
                return None

        credentials = Credentials(
            username=extract(property_paths.username),
            password=extract(property_paths.password),
        )
        has_credentials = credentials.username is not None or credentials.password is not None

        return Configuration(
            host=extract(property_paths.host),
            port=_to_int(extract(property_paths.port)),
            database=extract(property_paths.database),
            credentials=credentials if has_credentials else None,
        )

    @staticmethod
    def from_properties_file(
            file_path: str,
            property_paths: PropertiesFilePropertyPaths = PropertiesFilePropertyPaths()
    ) -> Configuration:
        props = Properties()
        with open(file_path, "rb") as f:
            props.load(f)

        def safe_get(key: str) -> Optional[str]:
            item = props.get(key)
            return item.data if item else None

        credentials = Credentials(
            username=safe_get(property_paths.username),
            password=safe_get(property_paths.password),
        )
        has_credentials = credentials.username is not None or credentials.password is not None

        return Configuration(
            host=safe_get(property_paths.host),
            port=_to_int(safe_get(property_paths.port)),
            database=safe_get(property_paths.database),
            credentials=credentials if has_credentials else None,
        )

    @staticmethod
    def from_ini_file(file_path: str, property_paths: IniPropertyPaths = IniPropertyPaths()) -> Configuration:
        config = ConfigParser()
        config.read(file_path)
        section = property_paths.section

        def safe_get(key: str) -> Optional[str]:
            try:
                return config.get(section, key)
            except Exception:
                return None

        credentials = Credentials(
            username=safe_get(property_paths.username),
            password=safe_get(property_paths.password),
        )
        has_credentials = credentials.username is not None or credentials.password is not None

        return Configuration(
            host=safe_get(property_paths.host),
            port=_to_int(safe_get(property_paths.port)),
            database=safe_get(property_paths.database),
            credentials=credentials if has_credentials else None,
        )

    @staticmethod
    def from_environment_variables(property_paths: EnvironmentVariables = EnvironmentVariables()) -> Configuration:
        def safe_env(var: str) -> Optional[str]:
            return os.environ.get(var)

        credentials = Credentials(
            username=safe_env(property_paths.username),
            password=safe_env(property_paths.password),
        )
        has_credentials = credentials.username is not None or credentials.password is not None

        return Configuration(
            host=safe_env(property_paths.host),
            port=_to_int(safe_env(property_paths.port)),
            database=safe_env(property_paths.database),
            credentials=credentials if has_credentials else None,
        )


def _to_int(value: Optional[str]) -> Optional[int]:
    try:
        return int(value) if value is not None else None
    except ValueError:
        return None
