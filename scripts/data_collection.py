import os
import requests
import pandas as pd
import json
from sqlalchemy import create_engine

API_KEY = os.environ["FOOTBALL_DATA_API_KEY"]
COMPETITION_CODE = "ELC"  # Championship

def fetch_matches():
    url = f"http://api.football-data.org/v4/competitions/{COMPETITION_CODE}/matches"
    response = requests.get(url, headers={"X-Auth-Token": API_KEY})
    data = response.json()

    # Converter para DataFrame e normalizar campos aninhados
    matches = pd.json_normalize(
        data["matches"],
        sep="_",
        meta=[
            "id",
            "utcDate",
            "status",
            ["homeTeam", "name"],
            ["awayTeam", "name"],
            ["score", "fullTime", "home"],
            ["score", "fullTime", "away"]
        ]
    )

    # Selecionar colunas essenciais
    cols = [
        "id",
        "utcDate",
        "status",
        "homeTeam_name",
        "awayTeam_name",
        "score_fullTime_home",
        "score_fullTime_away",
        "matchday",
        "season_startDate",
        "season_endDate"
    ]
    matches = matches[cols]

    # Converter dados ausentes para 0 (evitar tipos None)
    matches = matches.fillna(0)

    # Salvar em SQLite
    engine = create_engine("sqlite:///data/database/matches.db")
    matches.to_sql("championship_matches", engine, if_exists="replace", index=False)

if __name__ == "__main__":
    fetch_matches()