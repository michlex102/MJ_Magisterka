from kafka import KafkaConsumer
import json
import sys

# --- KONFIGURACJA ---
TOPIC_NAME = 'flight-positions'
GROUP_ID = 'testowa_grupa_konsumencka_v2' # Zmieniłem ID, żeby czytał od początku

print("📡 [KONSUMENT] Uruchamianie monitora lotów...")
print(f"   Nasłuchuję tematu: '{TOPIC_NAME}'")
print("   Wciśnij Ctrl+C, aby zakończyć.\n")

try:
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest', 
        enable_auto_commit=True,
        group_id=GROUP_ID,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
except Exception as e:
    print(f"❌ Błąd połączenia z Kafką: {e}")
    sys.exit(1)

print("✅ Połączono! Czekam na pakiety danych...\n")

counter = 0

try:
    for message in consumer:
        data = message.value
        counter += 1
        
        # --- MAPOWANIE DANYCH WG TWOJEJ SPECYFIKACJI ---
        
        # Czas snapshotu (np. 080000)
        time_stamp = data.get('snapshot_time', 'N/A')
        
        # Identyfikacja (Callsign jest ważniejszy dla człowieka, Hex dla maszyny)
        # Używamy .strip(), bo callsign w CSV często ma spacje na końcu "LOT123   "
        callsign = str(data.get('flight', 'N/A')).strip()
        hex_id = data.get('hex', 'N/A')
        
        # Jeśli nie ma Callsign (np. prywatny samolot), pokaż Hex
        identyfikator = callsign if callsign and callsign != 'nan' else f"HEX:{hex_id}"

        # Pozycja i Wysokość
        lat = data.get('lat', 0.0)
        lon = data.get('lon', 0.0)
        alt = data.get('alt_baro', 0) # Wysokość barometryczna (standard lotniczy)
        
        # Prędkość i Dystans
        speed_knots = data.get('gs', 0) # Węzły
        dist_km = data.get('distance_km', 0.0) # Twoja wyliczona odległość

        # Formatowanie wyjścia - jedna linia na jeden samolot
        # Używamy f-string z formatowaniem szerokości (np. <10), żeby tabelka była równa
        print(
            f"[{counter:04d}] "
            f"🕒 {time_stamp} | "
            f"✈️ {identyfikator:<8} | "
            f"📍 {lat:.4f}, {lon:.4f} | "
            f"🏔️ {alt:>5} ft | "
            f"🚀 {speed_knots:>3.0f} kts | "
            f"📏 {dist_km:>5.1f} km od WAW"
        )

except KeyboardInterrupt:
    print("\n🛑 Zatrzymano Konsumenta.")
    consumer.close()