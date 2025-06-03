from kafka import KafkaConsumer
import json
import pandas as pd
from datetime import datetime
import os

TOPIC = "fitbit"
SERVER = "localhost:9092"  # ← WAŻNE: poprawiona wartość!
CSV_FILE = "anomalie.csv"
STATS_FILE = "statystyki.csv"

print("👂 Konsument CSV z analizą uruchomiony...")

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[SERVER],
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="fitbit-anomaly-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

# Inicjalizacja plików jeśli nie istnieją
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=[
        "Id", "ActivityDate", "TotalSteps", "Calories", "VeryActiveMinutes", "Powody", "created_at"
    ]).to_csv(CSV_FILE, index=False)

if not os.path.exists(STATS_FILE):
    pd.DataFrame(columns=[
        "timestamp", "liczba_anomalii", "srednia_kroki", "mediana_kroki",
        "srednia_kalorie", "mediana_kalorie", "srednia_aktywnosc", "mediana_aktywnosc"
    ]).to_csv(STATS_FILE, index=False)

for message in consumer:
    data = message.value
    anomaly = False
    reasons = []

    if data["TotalSteps"] > 22000:
        anomaly = True
        reasons.append("dużo kroków")
    if data["Calories"] > 1800:
        anomaly = True
        reasons.append("dużo kalorii")
    if data["VeryActiveMinutes"] == 0:
        anomaly = True
        reasons.append("brak aktywności")

    now = datetime.now().isoformat()

    if anomaly:
        print(f"⚠️ ANOMALIA: {data} | Powody: {', '.join(reasons)}")

        df = pd.read_csv(CSV_FILE)
        df.loc[len(df.index)] = [
            data["Id"], data["ActivityDate"], data["TotalSteps"],
            data["Calories"], data["VeryActiveMinutes"],
            "; ".join(reasons), now
        ]
        df.to_csv(CSV_FILE, index=False)

        # Statystyki
        stats = {
            "timestamp": now,
            "liczba_anomalii": len(df),
            "srednia_kroki": round(df["TotalSteps"].mean(), 2),
            "mediana_kroki": round(df["TotalSteps"].median(), 2),
            "srednia_kalorie": round(df["Calories"].mean(), 2),
            "mediana_kalorie": round(df["Calories"].median(), 2),
            "srednia_aktywnosc": round(df["VeryActiveMinutes"].mean(), 2),
            "mediana_aktywnosc": round(df["VeryActiveMinutes"].median(), 2),
        }

        df_stats = pd.read_csv(STATS_FILE)
        df_stats.loc[len(df_stats.index)] = list(stats.values())
        df_stats.to_csv(STATS_FILE, index=False)
    else:
        print(f"✔️ OK: {data}")
