from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class ConfigAPI(BaseSettings):
    api_id: int
    api_hash: str

keys = ConfigAPI(api_id=os.environ.get('api_id'), api_hash=os.environ.get('api_hash'))
