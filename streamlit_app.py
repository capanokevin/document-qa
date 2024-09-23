import streamlit as st
import openai
import pandas as pd
import io

# Configura la chiave API di OpenAI dai secrets di Streamlit
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Configurazione della pagina
st.set_page_config(page_title="AI Dataset Generator", layout="wide")

# Stile personalizzato con CSS
st.markdown("""
    <style>
    body {
        background-color: #000000;
        color: #FFFFFF;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stTextArea textarea {
        background-color: transparent;
        border: 1px solid #FFFFFF;
        color: #FFFFFF;
        height: 150px;
    }
    .stButton>button {
        background-color: #1E1E1E;
        color: #FFFFFF;
        border-radius: 5px;
    }
    .stDataFrame {
        border-radius: 10px;
    }
    .dataframe {
        border-collapse: separate;
        border-spacing: 0;
        border: 1px solid #FFFFFF;
        border-radius: 10px;
        overflow: hidden;
    }
    .dataframe thead th {
        background-color: #333333;
        padding: 10px;
    }
    .dataframe tbody td {
        padding: 8px;
    }
    .main-title {
        text-align: center;
        padding: 20px 0;
        font-size: 2.5em;
        font-weight: bold;
        color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# Titolo dell'applicazione
st.markdown("<h1 class='main-title'>🚀 AI-Powered Dataset Generator</h1>", unsafe_allow_html=True)

# Creazione di due colonne con proporzioni personalizzate
col1, col2 = st.columns([2, 3])

with col1:
    # Sezione di input dell'utente
    st.header("Describe Your Data Needs:")
    user_input = st.text_area("Write here...", height=200)
    
    if st.button("Generate Dataset"):
        if user_input.strip() != "":
            with st.spinner("Generating dataset..."):
                # Chiamata all'API di OpenAI per elaborare l'input dell'utente
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an assistant that helps users create datasets based on their needs. When providing data, return it in CSV format without additional text."},
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
                    st.error("An error occurred while processing the data. Please ensure the AI returned data in the correct format.")
        else:
            st.warning("Please enter a description to proceed.")

with col2:
    # Sezione per visualizzare il dataset
    st.header("Your Generated Dataset:")
    if 'df' in st.session_state:
        st.dataframe(st.session_state['df'], use_container_width=True)
    else:
        # Tabella segnaposto
        placeholder_data = {
            'Column1': ['Sample', 'Data', 'Here'],
            'Column2': ['Will be', 'Replaced with', 'Generated Data'],
            'Column3': ['When You', 'Generate', 'A Dataset']
        }
        placeholder_df = pd.DataFrame(placeholder_data)
        st.dataframe(placeholder_df, use_container_width=True)

# Aggiunta di una sezione informativa sotto le colonne
st.markdown("---")
st.markdown("""
    ## How to Use This Tool
    1. **Describe Your Needs**: In the text area, describe the type of dataset you want to generate. Be as specific as possible about the columns, data types, and any patterns you want to see.
    2. **Generate**: Click the 'Generate Dataset' button to create your custom dataset using AI.
    3. **Review**: Your generated dataset will appear in the table on the right. You can scroll through it to review the data.
    4. **Iterate**: If the dataset doesn't meet your needs, try refining your description and generating again.
""")
