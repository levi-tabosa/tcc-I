import requests
import psycopg2
import os
import sys
import logging
import unicodedata
import time
import json
from datetime import datetime, date
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

try:
    import database.db as db
except ImportError:
    sys.path.append(os.getcwd())
    import database.db as db

BASE_URL = "https://api.portaldatransparencia.gov.br/api-de-dados" 

def api_get(url, params={'pagina': 1}):
    if params['pagina'] is None:
        params['pagina'] = 1

    headers = {
        "accept": "*/*",
        "chave-api-dados": API_KEY
    }

    try:
        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 429:
            logging.warning(f"Rate limited (429). Aguardando {wait}s...")
        else:
            logging.warning(f"Status {r.status_code} para {url}")
        return None
    except requests.exceptions.Timeout:
        logging.warning(f"Timeout")
    except Exception as e:
        logging.error(f"Error request: {e}")

