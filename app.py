import streamlit as st
from datetime import datetime
import pandas as pd
import os
import pyotp

# 1. Configurazione della pagina ottimizzata per lo schermo del cellulare
st.set_page_config(
    page_title="Badge Digitale Bagnini", 
    page_icon="🏖️", 
    layout="centered"
)

# 2. CHIAVE SEGRETA DI SICUREZZA (Standard TOTP)
# Deve essere identica a quella che userai nel file della segreteria.
CHIAVE_SEGRETA_TOTP = "JBSWY3DPEHPK3PXPJBSWY3DPEHPK3PXP"

# 3. Nome del file in cui verranno salvati tutti gli orari di ingresso e uscita
DB_FILE = "timbrature.csv"

# 4. Funzione interna per registrare i dati nel database Excel/CSV
def salva_timbratura(nome_bagnino, tipo_operazione):
    orario_attuale = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    nuovo_dato = pd.DataFrame([{
        "Bagnino": nome_bagnino, 
        "Tipo": tipo_operazione, 
        "Orario": orario_attuale
    }])
    
    if os.path.exists(DB_FILE):
        nuovo_dato.to_csv(DB_FILE, mode='a', header=False, index=False)
    else:
        nuovo_dato.to_csv(DB_FILE, index=False)
        
    st.success(f"✅ {tipo_operazione} registrato con successo per {nome_bagnino} alle ore {orario_attuale.split()[1]}!")

# 5. CONTROLLO DI SICUREZZA DEL QR CODE
query_params = st.query_params
token_ricevuto = query_params.get("token", None)

totp = pyotp.TOTP(CHIAVE_SEGRETA_TOTP, interval=30)

if token_ricevuto and totp.verify(token_ricevuto, valid_window=1):
    
    # --- SCHERMATA ATTIVA (Il bagnino è davanti al QR Code in segreteria) ---
    st.title("🏖️ Registro Presenze Stabilimento")
    st.success("📍 Presenza in segreteria verificata tramite QR Code attivo.")
    st.write("Seleziona il tuo nome e premi il pulsante corretto per timbrare.")

    # Lista dei bagnini modificabile
    lista_bagnini = [
        "Marco Rossi", 
        "Luca Bianchi", 
        "Alessio Verdi", 
        "Sofia Esposito"
    ]
    
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
    # --- SCHERMATA DI BLOCCO ---
    st.error("❌ Accesso Negato / QR Code Scaduto")
    st.warning("Non puoi accedere a questa pagina direttamente da questo link o usando una vecchia foto.")
    st.info("Per timbrare l'ingresso o l'uscita devi recarti fisicamente in segreteria e inquadrare il QR Code dinamico visualizzato sul monitor.")
