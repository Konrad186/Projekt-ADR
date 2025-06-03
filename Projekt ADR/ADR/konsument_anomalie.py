from kafka import KafkaConsumer
import json

TOPIC = "fitbit"
SERVER = "broker:9092"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=[SERVER],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='fitbit-anomaly-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("👂 Konsument uruchomiony. Czekam na dane...")

for message in consumer:
    data = message.value
    anomaly = False
    reasons = []

    if data['TotalSteps'] > 20000:
        anomaly = True
        reasons.append("bardzo dużo kroków")
    if data['Calories'] > 4500:
        anomaly = True
        reasons.append("bardzo dużo kalorii")
    if data['VeryActiveMinutes'] == 0:
        anomaly = True
        reasons.append("brak aktywności")

    if anomaly:
        print(f"⚠️ ANOMALIA: {data} | Powody: {', '.join(reasons)}")
    else:
        print(f"✔️ OK: {data}")
