import streamlit as st
import pyotp
import time

# Configurazione grafica per lo schermo della segreteria
st.set_page_config(page_title="Generatore QR Code Segreteria", layout="centered")

st.title("🖥️ Monitor Segreteria: Timbratura Bagnini")
st.write("Inquadra questo QR Code con la fotocamera del tuo cellulare per effettuare la timbratura.")

# Questa chiave deve essere IDENTICA a quella configurata nell'applicazione online
CHIAVE_SEGRETA_TOTP = "JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP" 

URL_BASE_APP = "https://streamlit.app"

URL_BASE_APP = "https://streamlit.app"

# Inizializza l'algoritmo del codice a tempo (scade ogni 30 secondi)
totp = pyotp.TOTP(CHIAVE_SEGRETA_TOTP, interval=30)
codice_attuale = totp.now()

# Costruisce il link sicuro temporaneo che verrà letto dallo smartphone
url_dinamico = f"{URL_BASE_APP}/?token={codice_attuale}"

# NUOVO SERVER QR CODE (Sostituito Google con QuickChart)
url_qr_code = f"https://quickchart.io/qr?text={url_dinamico}&size=300"

# Mostra il QR Code a tutto schermo sul monitor dell'ufficio
st.image(url_qr_code, caption="Il codice si aggiorna automaticamente ogni 30 secondi", use_container_width=False)

# Calcola il conto alla rovescia dei secondi rimanenti
tempo_rimanente = 30 - (int(time.time()) % 30)
st.metric(label="Il codice cambierà tra:", value=f"{tempo_rimanente} secondi")

# Ricarica lo schermo ogni 5 secondi per tenere aggiornato il timer e il QR code
time.sleep(5)
st.rerun()
