import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
import matplotlib.pyplot as plt


# ==============================
# CONFIG STREAMLIT
# ==============================
st.set_page_config(
    page_title="DHT Firebase Monitor",
    layout="wide"
)

st.title("📡 Surveillance Température & Humidité (Firebase)")

# ==============================
# FIREBASE CONFIG
# ==============================
FIREBASE_URL = "https://projet-final-2b542-default-rtdb.europe-west1.firebasedatabase.app/"

REFRESH_INTERVAL = 2  # secondes

# ==============================
# INITIALISATION DES DONNÉES
# ==============================
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["time", "temperature", "humidity"]
    )

# ==============================
# FONCTION DE LECTURE FIREBASE
# ==============================
def read_firebase():
    try:
        response = requests.get(FIREBASE_URL, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erreur Firebase : {e}")
        return None

# ==============================
# BOUCLE TEMPS RÉEL
# ==============================
placeholder = st.empty()

while True:
    data = read_firebase()

    if data and "temperature" in data and "humidity" in data:
        new_row = {
            "time": datetime.now(),
            "temperature": data["temperature"],
            "humidity": data["humidity"]
        }

        st.session_state.data = pd.concat(
            [st.session_state.data, pd.DataFrame([new_row])],
            ignore_index=True
        )

        # Garde seulement les 100 dernières valeurs
        st.session_state.data = st.session_state.data.tail(100)

    with placeholder.container():
        col1, col2 = st.columns(2)

        # -------- GRAPHE TEMPÉRATURE --------
        with col1:
            st.subheader("🌡️ Température (°C)")
            fig, ax = plt.subplots()
            ax.plot(
                st.session_state.data["time"],
                st.session_state.data["temperature"]
            )
            ax.set_xlabel("Temps")
            ax.set_ylabel("Température (°C)")
            ax.grid(True)
            st.pyplot(fig)

        # -------- GRAPHE HUMIDITÉ --------
        with col2:
            st.subheader("💧 Humidité (%)")
            fig, ax = plt.subplots()
            ax.plot(
                st.session_state.data["time"],
                st.session_state.data["humidity"]
            )
            ax.set_xlabel("Temps")
            ax.set_ylabel("Humidité (%)")
            ax.grid(True)
            st.pyplot(fig)

    time.sleep(REFRESH_INTERVAL)
