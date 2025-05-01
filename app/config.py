import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY =  os.getenv('GEMINI_API_KEY')
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

import logging

logging.basicConfig(
    filename="app/app.log",
    level=logging.INFO,  # or DEBUG, WARNING, etc.
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
