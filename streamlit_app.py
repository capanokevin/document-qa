import streamlit as st
import openai
import pandas as pd
import io

# Configura la chiave API di OpenAI dai secrets di Streamlit
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Configurazione della pagina
st.set_page_config(page_title="Build Your Dataset with our AI", layout="wide")

# Stile personalizzato con CSS
st.markdown("""
    <style>
    body {
        background-color: #000000;
        color: #FFFFFF;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stTextArea textarea {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    </style>
    """, unsafe_allow_html=True)

# Titolo dell'applicazione
st.title("🚀 Build Your Dataset with our AI")

# Creazione di due colonne
col1, col2 = st.columns(2)

with col1:
    # Sezione di input dell'utente
    st.header("Descrivi le tue esigenze di dati:")
    user_input = st.text_area("Scrivi qui...", height=300)

    if st.button("Genera Dataset"):
        if user_input.strip() != "":
            with st.spinner("Generazione del dataset in corso..."):
                # Chiamata all'API di OpenAI per elaborare l'input dell'utente
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Sei un assistente che aiuta gli utenti a creare dataset basati sulle loro esigenze. Quando fornisci i dati, restituiscili in formato CSV senza testo aggiuntivo."},
                        {"role": "user", "content": user_input}
                    ]
                )

                # Estrazione della risposta dell'assistente
                reply = response['choices'][0]['message']['content']

                # Parsing della risposta CSV in un DataFrame
                try:
                    csv_data = io.StringIO(reply)
                    df = pd.read_csv(csv_data)
                    # Memorizzazione del DataFrame nello stato della sessione
                    st.session_state['df'] = df
                except Exception as e:
                    st.error("Si è verificato un errore nell'elaborazione dei dati. Assicurati che l'AI abbia restituito i dati nel formato corretto.")
        else:
            st.warning("Per favore, inserisci una descrizione per procedere.")

with col2:
    # Sezione per visualizzare il dataset
    st.header("Il Tuo Dataset:")
    if 'df' in st.session_state:
        st.table(st.session_state['df'])
    else:
        # Tabella segnaposto
        placeholder_data = {
            'Colonna1': ['-', '-', '-'],
            'Colonna2': ['-', '-', '-'],
            'Colonna3': ['-', '-', '-']
        }
        placeholder_df = pd.DataFrame(placeholder_data)
        st.table(placeholder_df)
