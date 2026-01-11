# Praca Magisterska: Analiza czynników determinujących niezadowolenie pasażerów oraz wspomaganie procesów operacyjnych

## Przegląd Projektu
Niniejsze repozytorium zawiera kod źródłowy projektu realizowanego w ramach pracy magisterskiej pod tytułem roboczym.: "Analiza czynników determinujących niezadowolenie pasażerów oraz wspomaganie procesów operacyjnych w celu poprawy wskaźnika NPS w linii lotniczej".

Projekt składa się z dwóch integralnych części:
1.  **Analiza ML i XAI:** Pipeline przetwarzania danych ankietowych (NPS), imputacji braków oraz trenowania modeli klasyfikacyjnych (Random Forest, XGBoost, Sieci Neuronowe) w celu identyfikacji przyczyn niezadowolenia pasażerów. Wykorzystano metody interpretowalności modeli (SHAP).
2.  **Dashboard Operacyjny (Real-Time):** Prototyp systemu wspierania decyzji dla działu Disruption Management. System wykorzystuje Apache Kafka do symulacji strumieniowania danych w czasie rzeczywistym (na bazie ADS-B) oraz framework Streamlit do wizualizacji i priorytetyzacji lotów wysokiego ryzyka.

## Struktura Repozytorium

### Folder Codes
Folder zawiera skrypty Python podzielone według funkcjonalności:

* **NPS Main.ipynb**
    Główny potok przetwarzania danych (pipeline). Obejmuje wczytanie surowych danych, czyszczenie, obsługę braków danych (kNN dla braków losowych MAR, imputacja średnią dla braków strukturalnych), analizę korelacji oraz podział na zbiory treningowe, walidacyjne i testowe.

* **NPS Analysis.ipynb**
    Część analityczno-modelowa. Zawiera trening modeli (Drzewa Decyzyjne, Random Forest, XGBoost, Sieci Neuronowe), ewaluację wyników oraz szczegółową analizę XAI (SHAP) identyfikującą kluczowe czynniki wpływające na detrakcję (np. wpływ procesu transferowego na lotach Long Haul).

* **NPS-Sentyment.ipynb**
    Moduł NLP (Natural Language Processing). Wykorzystuje model XLM-RoBERTa do analizy sentymentu komentarzy pasażerów w celu identyfikacji tzw. "Silent Detractors" (osób z oceną neutralną, ale negatywnym komentarzem).

* **Dashboard.py**
    Kod aplikacji wizualizacyjnej opartej na bibliotece Streamlit. Odpowiada za odbieranie danych z Kafki, wizualizację pozycji samolotów na mapie oraz obliczanie priorytetów biznesowych dla lotów zagrożonych.

* **Flight_Data_Download.py**
    Skrypt pomocniczy służący do pobierania historycznych danych ADS-B z serwisu ADS-B Exchange, wykorzystywanych następnie do symulacji.

* **test_producer.py**
    Symulator producenta danych (Kafka Producer). Odczytuje historyczny plik CSV z danymi lotniczymi i wysyła je do tematu Kafki w pętlach czasowych, symulując napływ danych z transponderów w czasie rzeczywistym.

* **test_consumer.py**
    Skrypt testowy konsumenta (Kafka Consumer), służący do weryfikacji poprawności odbierania komunikatów przed uruchomieniem pełnego Dashboardu.

### Folder Data
Folder zawiera zbiory danych oraz pliki metadanych.
*Uwaga: Część danych handlowych oraz surowe dane osobowe zostały usunięte z repozytorium ze względu na umowy o poufności (NDA).*

* **NPS_final/**: Katalog z przetworzonymi zbiorami gotowymi do modelowania (X_train, y_train, X_val, etc.).
* **ax_arrivals_20251201.csv**: Zbiór pomocniczy identyfikujący porty początkowe i docelowe dla filtrowania danych ADS-B.
* **ID_Col.xlsx**: Plik konfiguracyjny z flagami zmiennych, służący do wstępnej filtracji cech ze zbioru NPS.
* **loty_waw_8_23_20251201.csv**: Próbka danych ADS-B (loty dolatujące do WAW, 1 grudnia 2025, godz. 08:00-23:00) stanowiąca wsad do symulacji Real-Time.
* **NPS_2025 opis kolumn**: Dokumentacja zmiennych występujących w ankiecie NPS.
* **nps_sentiment_results.csv**: Wynik działania modułu NLP, zawierający flagi sentymentu dla poszczególnych rekordów.

### Pliki w katalogu głównym
* **docker-compose.yml**: Plik konfiguracyjny infrastruktury Docker. Definiuje usługi Zookeeper oraz Apache Kafka niezbędne do uruchomienia warstwy przesyłu danych.
* **.gitignore**: Lista plików i folderów ignorowanych przez system kontroli wersji.