FROM python:3.9-slim

WORKDIR /app

COPY producent_projekt.py .
COPY dailyActivity_merged.csv .

RUN pip install kafka-python pandas

CMD ["python", "producent_projekt.py"]
