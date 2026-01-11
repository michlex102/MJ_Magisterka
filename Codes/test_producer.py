import pandas as pd
from kafka import KafkaProducer
import json
import time
import os


SPEED_FACTOR = 1.0       # 1.0 = czas rzeczywisty (czeka 5s), 10.0 = 10x szybciej (czeka 0.5s)
TOPIC_NAME = 'flight-positions'
CSV_FILENAME = 'loty_waw_8_10_20251201.csv' 

# Inicjalizacja Producenta
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x, default=str).encode('utf-8')
)

def run_producer():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', CSV_FILENAME)

    print(f"Szukam danych w: {data_path}")

    if not os.path.exists(data_path):
        print("BŁĄD: Nie znaleziono pliku! Sprawdź folder 'data' i nazwę pliku.")
        return

    print("Wczytuję i przetwarzam dane...")
    try:
        df = pd.read_csv(data_path)
    except Exception as e:
        print(f"Błąd odczytu: {e}")
        return

    # 3. Sortowanie danych po czasie
    if 'snapshot_time' in df.columns:
        df = df.sort_values(by='snapshot_time')
    else:
        print("BŁĄD: Nie znaleziono kolumny 'snapshot_time' w pliku CSV!")
        print(f"   Dostępne kolumny: {list(df.columns)}")
        return

    # Grupowanie w paczki danych
    grouped_packets = df.groupby('snapshot_time')

    print(f"Znaleziono {len(grouped_packets)} unikalnych paczek czasowych (snapshotów).")
    print(f"Start symulacji (Speed: {SPEED_FACTOR}x, Interwał bazowy: 5s)")
    print("   (Ctrl+C aby zatrzymać)")

    try:
        # Iterujemy po każdej grupie (paczce)
        for timestamp, packet_df in grouped_packets:
            
            start_process = time.time()
            record_count = len(packet_df)

            # wysyłanie paczki
            # Iterujemy po wszystkich samolotach w tym jednym snapshocie
            for _, row in packet_df.iterrows():
                message = row.to_dict()
                producer.send(TOPIC_NAME, value=message)
            
            producer.flush()
            
            print(f" -> Paczka {timestamp}: Wysłano {record_count} lotów.")

            # Skoro dane są co 5 sekund, to czekamy 5 sekund (podzielone przez przyspieszenie)
            wait_time = 5.0 / SPEED_FACTOR
            time.sleep(wait_time)

    except KeyboardInterrupt:
        print("\n Zatrzymano symulację.")
    finally:
        producer.close()

if __name__ == "__main__":
    run_producer()