import streamlit as st
from kafka import KafkaConsumer
import pandas as pd
import json
import time
import pydeck as pdk 

st.set_page_config(
    page_title="Radar Lotniczy Live",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    </style>
""", unsafe_allow_html=True)

st.title("System Monitorowania Lotów (Real-Time)")


# Kontener na metryki
metrics_container = st.container()
col1, col2, col3, col4 = metrics_container.columns(4)

with col1:
    kpi1_slot = st.empty()
with col2:
    kpi2_slot = st.empty()
with col3:
    kpi3_slot = st.empty()
with col4:
    kpi4_slot = st.empty()

# Slot na mapę (pod spodem)
map_placeholder = st.empty()

# Połączenie z kafką
TOPIC_NAME = 'flight-positions'
GROUP_ID = 'streamlit_dashboard_final_v1' # Nowa grupa dla pewności

@st.cache_resource
def init_consumer():
    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='latest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            group_id=GROUP_ID
        )
        return consumer
    except Exception as e:
        st.error(f"Błąd Kafki: {e}")
        return None

consumer = init_consumer()

if not consumer:
    st.stop()

if 'flights_data' not in st.session_state:
    st.session_state['flights_data'] = {}

try:
    while True:
        raw_msgs = consumer.poll(timeout_ms=500)

        if raw_msgs:
            for topic_partition, messages in raw_msgs.items():
                for msg in messages:
                    new_data = msg.value
                    plane_id = new_data.get('hex') or new_data.get('flight')
                    st.session_state['flights_data'][plane_id] = new_data

            df = pd.DataFrame(st.session_state['flights_data'].values())

            if 'alt_baro' in df.columns:
                df['alt_baro'] = pd.to_numeric(df['alt_baro'], errors='coerce')
            if 'lat' in df.columns:
                df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
            if 'lon' in df.columns:
                df['lon'] = pd.to_numeric(df['lon'], errors='coerce')

            # Funkcja decydująca o kolorze: [R, G, B, A]
            def get_color(row):
                # Jeśli wysokość to NaN (czyli było "ground") lub 0 -> CZERWONY
                # Sprawdzenie kolumny 'on_ground' jeśli istnieje w danych
                is_ground = False
                
                if 'on_ground' in row and str(row['on_ground']).lower() == 'true':
                    is_ground = True
                elif pd.isna(row.get('alt_baro')) or row.get('alt_baro') <= 0:
                    is_ground = True
                
                if is_ground:
                    return [255, 0, 0, 200]  # Czerwony, bardziej widoczny
                return [0, 255, 0, 160]      # Zielony

            if not df.empty:
                df['fill_color'] = df.apply(get_color, axis=1)

            total_planes = len(df)
            last_time = df['snapshot_time'].max() if not df.empty and 'snapshot_time' in df.columns else "---"
            avg_alt = df['alt_baro'].mean() if not df.empty and 'alt_baro' in df.columns else 0

            kpi1_slot.metric("Aktywne samoloty", total_planes)
            kpi2_slot.metric("Czas symulacji", str(last_time))
            kpi3_slot.metric("Średnia wys. [ft]", f"{avg_alt:.0f}")
            kpi4_slot.metric("Status Systemu", "🟢 Online")

            # Mapa
            if not df.empty and 'lat' in df.columns and 'lon' in df.columns:
                map_df = df.dropna(subset=['lat', 'lon'])
                
                layer = pdk.Layer(
                    "ScatterplotLayer",
                    data=map_df,
                    get_position='[lon, lat]',
                    get_color='fill_color', # <--- ZMIANA: Czytaj z kolumny 'fill_color'
                    get_radius=1000,
                    pickable=True
                )

                # Ustawienia widoku
                view_state = pdk.ViewState(
                    latitude=52.0693, longitude=19.4803, zoom=5.5, pitch=0
                )

                r = pdk.Deck(
                    layers=[layer],
                    initial_view_state=view_state,
                    map_style='https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
                    tooltip={"text": "Lot: {flight}\nHeks: {hex}\nWys: {alt_baro} ft"}
                )
                
                map_placeholder.pydeck_chart(r, use_container_width=True, height=800)

        else:
            kpi4_slot.metric("Status Systemu", "🟡 Oczekiwanie...")
            time.sleep(0.1)

except KeyboardInterrupt:
    print("Zatrzymano.")