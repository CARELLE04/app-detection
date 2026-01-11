import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Charger la clé Firebase depuis les secrets Streamlit
cred_json = os.getenv('FIREBASE_CREDENTIALS_PATH')  # Récupérer la clé JSON depuis les secrets
cred = credentials.Certificate(cred_json)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://firevent-iot-ea63b-default-rtdb.firebaseio.com/'  # URL de votre base Firebase
})

# Récupérer les données de Firebase
def get_data_from_firebase():
    ref = db.reference('mesures_esp32')  # Référence au nœud Firebase
    data = ref.get()
    
    # Convertir les données en DataFrame pour faciliter l'analyse
    df = pd.DataFrame.from_dict(data, orient='index')
    df['timestamp'] = pd.to_datetime(df['timestamp'])  # Convertir le timestamp en format DateTime
    return df

# Visualisation des données avec Streamlit
def plot_graphs(df):
    # Graphique de la température
    fig_temp, ax_temp = plt.subplots()
    ax_temp.plot(df['timestamp'], df['temperature'], color='r', label='Température (°C)')
    ax_temp.set_title('Variation de la Température')
    ax_temp.set_xlabel('Date')
    ax_temp.set_ylabel('Température (°C)')
    ax_temp.legend()

    # Graphique de l'humidité
    fig_humidity, ax_humidity = plt.subplots()
    ax_humidity.plot(df['timestamp'], df['humidity'], color='b', label='Humidité (%)')
    ax_humidity.set_title('Variation de l\'Humidité')
    ax_humidity.set_xlabel('Date')
    ax_humidity.set_ylabel('Humidité (%)')
    ax_humidity.legend()

    # Affichage des graphiques dans Streamlit
    st.pyplot(fig_temp)
    st.pyplot(fig_humidity)

# Interface Streamlit
def main():
    st.title('Visualisation des Données de Température et d\'Humidité')

    # Récupérer les données de Firebase
    df = get_data_from_firebase()

    # Afficher les 5 premières lignes des données
    st.write("Données de la base Firebase :")
    st.write(df.head())

    # Afficher les graphiques
    plot_graphs(df)

if __name__ == "__main__":
    main()
