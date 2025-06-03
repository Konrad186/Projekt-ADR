
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Wczytanie danych
df_anom = pd.read_csv("anomalie.csv")
df_stats = pd.read_csv("statystyki.csv")

# Czyszczenie i formatowanie dat
df_anom.drop_duplicates(inplace=True)
df_anom.dropna(inplace=True)

# Jeśli kolumna daty istnieje, konwertuj ją
if "ActivityDate" in df_anom.columns:
    df_anom["ActivityDate"] = pd.to_datetime(df_anom["ActivityDate"], errors='coerce')

# Wykres 1: Korelacja kroków vs kalorii z kolorem wg aktywnych minut
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_anom, x="TotalSteps", y="Calories", hue="VeryActiveMinutes", palette="viridis")
plt.title("Korelacja: Kroki vs Kalorie (kolor: aktywne minuty)")
plt.xlabel("TotalSteps")
plt.ylabel("Calories")
plt.tight_layout()
plt.savefig("wykres_kroki_kalorie.png")
plt.close()

# Wykres 2: Rozkład aktywnych minut
plt.figure(figsize=(10, 6))
sns.histplot(df_anom["VeryActiveMinutes"], bins=20, kde=True)
plt.title("Rozkład bardzo aktywnych minut")
plt.xlabel("VeryActiveMinutes")
plt.tight_layout()
plt.savefig("wykres_aktywnosc.png")
plt.close()

# Wykres 3: Boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_anom[["TotalSteps", "Calories", "VeryActiveMinutes"]])
plt.title("Boxplot: TotalSteps, Calories, VeryActiveMinutes")
plt.tight_layout()
plt.savefig("wykres_boxplot.png")
plt.close()

# Statystyki ogólne
print("\n📊 Ostatnie statystyki:")
print(df_stats.tail(5))

print("\n✅ Wykresy zapisane jako PNG.")
