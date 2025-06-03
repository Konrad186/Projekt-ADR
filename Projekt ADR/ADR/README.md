## Opis projektu

Projekt realizowany w ramach zadania zespołowego. Celem było zbudowanie systemu analitycznego do monitorowania aktywności użytkowników (na podstawie danych z aplikacji Fitbit), wykrywania anomalii, generowania statystyk oraz wizualizacji danych.

## Struktura projektu

├── producent_projekt.py         # Producent Kafka – wysyła dane z CSV
├── konsument_anomalie_csv.py   # Konsument Kafka – zapisuje anomalie/statystyki
├── analiza.py                   # Analiza danych i generowanie wykresów
├── anomalie.csv                 # Wykryte anomalie (output)
├── statystyki.csv              # Statystyki dzienne (output)
├── wykres_*.png                # Wygenerowane wykresy
├── analiza_biznesowa_fitbit.docx  # Raport z wnioskami biznesowymi
├── docker-compose.yml          # Konfiguracja Kafka + Zookeeper
├── Dockerfile                  # Obraz producenta (opcjonalnie)
└── README.md                   # Instrukcja

## Instrukcja uruchomienia (kolejność)

1. Uruchom środowisko Kafka:

docker-compose up

Pozostaw terminal z Dockerem uruchomiony w tle.

2. Uruchom producenta:

python producent_projekt.py

Producent wysyła dane z pliku dailyActivity_merged.csv do tematu Kafka "fitbit".

3. Uruchom konsumenta:

python konsument_anomalie_csv.py

Konsument zapisuje anomalie i statystyki do plików .csv.

4. Po zebraniu danych – uruchom analizę:

python analiza.py

Wygeneruje wykresy PNG i wypisze statystyki.

## Wykresy

- wykres_kroki_kalorie.png – korelacja kroków i kalorii
- wykres_aktywnosc.png – rozkład aktywnych minut
- wykres_boxplot.png – rozrzut cech aktywności

## Plik Word

analiza_biznesowa_fitbit.docx zawiera gotowe wnioski i rekomendacje

## Technologie

- Python (Kafka, Pandas, Seaborn, Matplotlib)
- Docker (Kafka, Zookeeper)
- Git (wersjonowanie projektu)
- CSV (wymiana danych między komponentami)

## Autorzy

Zespół 3 – projekt zespołowy: analiza i raportowanie w czasie rzeczywistym.
