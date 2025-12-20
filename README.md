## 🎯 Cel projektu
Projekt badawczy realizowany w ramach pracy magisterskiej, mający na celu stworzenie systemu wsparcia decyzji operacyjnych dla portu lotniczego Warszawa-Okęcie (WAW). System integruje dane o pozycjach samolotów (ADS-B) z analizą satysfakcji pasażerów oraz ich znaczeniem rynkowym (wskaźnik HHI).

---

## 👨‍🏫 Instrukcja dla Promotora

Poniżej znajduje się ścieżka uruchomienia poszczególnych modułów systemu:

### 1️⃣ Krok 1: Przygotowanie środowiska
Zaleca się stworzenie izolowanego środowiska wirtualnego:

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
### 2️⃣ Krok 2: Analiza Predykcyjna (Model ML)
Proces budowy modelu i analizy danych znajduje się w notebooku:
Ścieżka: Codes/nps_analysis.ipynb
Opis: Czyszczenie danych NPS, trening modelu, analiza istotności cech (SHAP).

### 3️⃣ Krok 3: Infrastruktura i Strumieniowanie
Uruchomienie brokera wiadomości Kafka (wymaga zainstalowanego Docker Desktop):
```bash
docker-compose up -d
```
Odpalić kod Flight_Data_Download w celu pobrania danych ze strony 

### 4️⃣ Krok 4: Symulacja i Dashboard
W osobnych oknach terminala należy uruchomić:
python Codes/kafka_producer.py
streamlit run Codes/dashboard.py

## 📂 Struktura Repozytorium
Codes/ – notebooki analityczne oraz skrypty systemowe.

Data/ – zbiory danych i słowniki rynkowe.

requirements.txt – specyfikacja bibliotek Python.

docker-compose.yml – konfiguracja kontenera Kafka.

# Autor: Michał Jamroży 113984

# Promotor: Michał Bernadelli

# Uczelnia: Szkoła Główna Handlowa w Warszawie