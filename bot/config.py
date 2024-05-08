from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

import os

current_directory = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_directory, '..'))
datebasePath = os.path.join(project_root, 'db', 'users.db')
siteDatebasePath = os.path.join(project_root, 'db', 'site.db')

class Settings(BaseSettings):
    bot_token: SecretStr
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

config = Settings()