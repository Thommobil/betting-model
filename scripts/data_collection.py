import os
import requests
import pandas as pd
from sqlalchemy import create_engine

# Configurar API Key
API_KEY = os.environ["FOOTBALL_DATA_API_KEY"]
COMPETITION_CODE = "ELC"  # Championship

def fetch_matches():
    url = f"http://api.football-data.org/v4/competitions/{COMPETITION_CODE}/matches"
    response = requests.get(url, headers={"X-Auth-Token": API_KEY})
    data = response.json()
    
    # Processar dados
    matches = pd.json_normalize(data["matches"])
    
    # Salvar em SQLite
    engine = create_engine("sqlite:///data/database/matches.db")
    matches.to_sql("championship_matches", engine, if_exists="replace", index=False)

if __name__ == "__main__":
    fetch_matches()