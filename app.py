import streamlit as st
from datetime import datetime
import pandas as pd
import os
import pyotp

st.set_page_config(page_title="Badge Digitale Bagnini", page_icon="🏖️", layout="centered")

CHIAVE_SEGRETA_TOTP = "JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP"
DB_FILE = "timbrature.csv"

def salva_timbratura(nome_bagnino, tipo_operazione):
    orario_attuale = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nuovo_dato = pd.DataFrame([{"Bagnino": nome_bagnino, "Tipo": tipo_operazione, "Orario": orario_attuale}])
    
    if os.path.exists(DB_FILE):
        nuovo_dato.to_csv(DB_FILE, mode='a', header=False, index=False)
    else:
        nuovo_dato.to_csv(DB_FILE, index=False)
        
    st.success(f"✅ {tipo_operazione} registrato con successo per {nome_bagnino} alle ore {orario_attuale.split()[1]}!")

# Controllo del gettone di sicurezza nell'URL dello smartphone
query_params = st.query_params
token_ricevuto = query_params.get("token", None)

totp = pyotp.TOTP(CHIAVE_SEGRETA_TOTP, interval=30)

if token_ricevuto and totp.verify(token_ricevuto, valid_window=1):
    st.title("🏖️ Registro Presenze Stabilimento")
    st.success("📍 Presenza in segreteria verificata tramite QR Code attivo.")
    
    lista_bagnini = ["Marco Rossi", "Luca Bianchi", "Alessio Verdi", "Sofia Esposito"]
    bagnino_selezionato = st.selectbox("Chi sei?", lista_bagnini)

    st.write("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 REGISTRA ENTRATA", use_container_width=True):
            salva_timbratura(bagnino_selezionato, "ENTRATA")

    with col2:
        if st.button("🛑 REGISTRA USCITA", use_container_width=True):
            salva_timbratura(bagnino_selezionato, "USCITA")
else:
    st.title("🔐 Area Riservata Direzione")
    st.warning("Per timbrare devi inquadrare il QR Code in segreteria.")
    st.write("---")
    st.subheader("Visualizza Resoconto Mensile (Solo Direzione)")
    
    password_inserita = st.text_input("Inserisci la password amministratore:", type="password")
    
    if password_inserita == "Spiaggia2026":
        st.success("🔓 Accesso consentito!")
        if os.path.exists(DB_FILE):
            df = pd.read_csv(DB_FILE)
            st.write("### 📅 Tutte le timbrature registrate:")
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 SCARICA FILE EXCEL / CSV",
                data=csv,
                file_name=f"resoconto_bagnini_{datetime.now().strftime('%m_%Y')}.csv",
                mime='text/csv',
            )
        else:
            st.info("Nessuna timbratura presente nel database al momento.")

