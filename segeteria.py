import streamlit as st
import pyotp
import time

st.set_page_config(page_title="Generatore QR Code Segreteria", layout="centered")

st.title("🖥️ Monitor Segreteria: Timbratura Bagnini")
st.write("Inquadra questo QR Code con la fotocamera del tuo cellulare per effettuare la timbratura.")

CHIAVE_SEGRETA_TOTP = "JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP" 

# URL PUBBLICO DEFINITIVO CHE ASSEGNEREMO ALL'APP DEI BAGNINI
URL_BASE_APP = "https://streamlit.app"

totp = pyotp.TOTP(CHIAVE_SEGRETA_TOTP, interval=30)
codice_attuale = totp.now()

url_dinamico = f"{URL_BASE_APP}/?token={codice_attuale}"
url_qr_code = f"https://quickchart.io{url_dinamico}&size=300"

st.image(url_qr_code, caption="Il codice si aggiorna automaticamente ogni 30 secondi", use_container_width=False)

tempo_rimanente = 30 - (int(time.time()) % 30)
st.metric(label="Il codice cambierà tra:", value=f"{tempo_rimanente} secondi")

time.sleep(5)
st.rerun()
