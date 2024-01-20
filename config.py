import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL') or ''
MONGO_DATABASE = os.getenv('MONGO_DATABASE') or ''
MONGO_TABLE = os.getenv('MONGO_TABLE') or ''

