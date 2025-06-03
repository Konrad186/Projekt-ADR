import pandas as pd
import json
import random
import socket
from datetime import datetime
from time import sleep
from kafka import KafkaProducer

# Łączenie do lokalnego brokera Kafka (działającego w Dockerze)
SERVER = "localhost:9092"
TOPIC = "fitbit"

# Czekanie na dostępność Kafki
def wait_for_kafka(host, port, retries=30):
    for i in range(retries):
        try:
            with socket.create_connection((host, port), timeout=2):
                print("✅ Kafka dostępna, startuję producenta.")
                return
        except OSError:
            print(f"❌ Kafka niedostępna, próba {i + 1}/{retries}...")
            sleep(2)
    raise Exception("Kafka nie wystartowała na czas.")

wait_for_kafka("localhost", 9092)

# Wczytaj dane z pliku CSV
df = pd.read_csv("dailyActivity_merged.csv")
df = df[['Id', 'TotalSteps', 'Calories', 'VeryActiveMinutes']]
df['ActivityDate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Jeśli za mało danych – generuj syntetyczne
def generate_synthetic_data(n=1000):
    synthetic = []
    for _ in range(n):
        entry = {
            "Id": random.randint(1000000000, 9999999999),
            "ActivityDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "TotalSteps": random.randint(0, 25000),
            "Calories": random.randint(300, 2000),
            "VeryActiveMinutes": random.randint(0, 180)
        }
        synthetic.append(entry)
    return pd.DataFrame(synthetic)

if len(df) < 1000:
    synthetic_df = generate_synthetic_data(n=1000 - len(df))
    df = pd.concat([df, synthetic_df], ignore_index=True)

# Tworzenie producenta Kafka
producer = KafkaProducer(
    bootstrap_servers=[SERVER],
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)

# Wysyłanie danych
try:
    while True:
        sample = df.sample(1).to_dict(orient="records")[0]
        sample['ActivityDate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        producer.send(TOPIC, value=sample)
        print(f"📤 Wysłano: {sample}")
        sleep(1)
except KeyboardInterrupt:
    print("⛔ Zatrzymano producenta.")
    producer.close()
