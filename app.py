import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import matplotlib.pyplot as plt

# --- INIT FIREBASE (une seule fois) ---
def init_firebase():
    if not firebase_admin._apps:
        cred_dict = eval(st.secrets["FIREBASE_SERVICE_ACCOUNT"])  # JSON string -> dict
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {
            "databaseURL": st.secrets["FIREBASE_DATABASE_URL"]
        })

init_firebase()

# --- LECTURE DATA ---
def get_data_from_firebase():
    ref = db.reference("mesures_esp32")
    data = ref.get()

    if not data:
        return pd.DataFrame()

    df = pd.DataFrame.from_dict(data, orient="index")

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    return df.sort_values("timestamp")

# --- GRAPHS ---
def plot_graphs(df):
    if df.empty:
        st.warning("Aucune donnée trouvée dans Firebase.")
        return

    # Température
    fig1, ax1 = plt.subplots()
    ax1.plot(df["timestamp"], df["temperature"])
    ax1.set_title("Variation de la Température")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Température (°C)")
    st.pyplot(fig1)

    # Humidité
    fig2, ax2 = plt.subplots()
    ax2.plot(df["timestamp"], df["humidity"])
    ax2.set_title("Variation de l'Humidité")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Humidité (%)")
    st.pyplot(fig2)

# --- UI ---
def main():
    st.title("Visualisation Température & Humidité (Firebase)")
    df = get_data_from_firebase()
    st.write("Aperçu des données :")
    st.dataframe(df.head())
    plot_graphs(df)

if __name__ == "__main__":
    main()
