import streamlit as st
import openai
import pandas as pd
import io
from streamlit_option_menu import option_menu

# Gestione dell'importazione di plotly
try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("Plotly non è disponibile. Alcune funzionalità di visualizzazione potrebbero essere limitate.")


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
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid #FFFFFF;
        color: #FFFFFF;
        height: 150px;
    }
    .stButton>button {
        background-color: #00d084;
        color: #000000;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00a067;
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
        font-size: 2.5em;
        font-weight: bold;
        color: #FFFFFF;
        margin-bottom: 20px;
    }
    .section-title {
        color: #00d084;
        font-size: 1.5em;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    .card {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Funzione per la pagina principale
def main_page():
    st.markdown("<h1 class='main-title'>AI Dataset Generator</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title'>Describe Your Data Needs</h2>", unsafe_allow_html=True)
        user_input = st.text_area("Be as specific as possible about the columns, data types, and patterns you want to see.", height=200)
        if st.button("Generate Dataset"):
            if user_input.strip() != "":
                with st.spinner("Generating dataset..."):
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are an assistant that helps users create datasets based on their needs. When providing data, return it in CSV format without additional text."},
                            {"role": "user", "content": user_input}
                        ]
                    )
                    reply = response['choices'][0]['message']['content']
                    try:
                        csv_data = io.StringIO(reply)
                        df = pd.read_csv(csv_data)
                        st.session_state['df'] = df
                        st.session_state['datasets_generated'] = st.session_state.get('datasets_generated', 0) + 1
                    except Exception as e:
                        st.error("An error occurred while processing the data. Please ensure the AI returned data in the correct format.")
            else:
                st.warning("Please enter a description to proceed.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title'>Generated Dataset</h2>", unsafe_allow_html=True)
        if 'df' in st.session_state:
            st.dataframe(st.session_state['df'], use_container_width=True)
        else:
            st.info("Your generated dataset will appear here.")
        st.markdown("</div>", unsafe_allow_html=True)

# Funzione per la pagina delle statistiche
def stats_page():
    st.markdown("<h1 class='main-title'>Dataset Statistics</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title'>Usage Statistics</h2>", unsafe_allow_html=True)
        datasets_generated = st.session_state.get('datasets_generated', 0)
        st.metric("Datasets Generated", datasets_generated)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title'>Recent Dataset Summary</h2>", unsafe_allow_html=True)
        if 'df' in st.session_state:
            df = st.session_state['df']
            st.write(f"Number of Rows: {len(df)}")
            st.write(f"Number of Columns: {len(df.columns)}")
            st.write("Column Types:")
            for col, dtype in df.dtypes.items():
                st.write(f"- {col}: {dtype}")
        else:
            st.info("Generate a dataset to see its summary here.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    if 'df' in st.session_state and PLOTLY_AVAILABLE:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='section-title'>Data Visualization</h2>", unsafe_allow_html=True)
        df = st.session_state['df']
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 1:
            x_axis = st.selectbox("Select X-axis", numeric_cols)
            y_axis = st.selectbox("Select Y-axis", [col for col in numeric_cols if col != x_axis])
            fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="white")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("The current dataset doesn't have enough numeric columns for visualization.")
        st.markdown("</div>", unsafe_allow_html=True)
    elif 'df' in st.session_state and not PLOTLY_AVAILABLE:
        st.warning("Plotly non è disponibile. La visualizzazione dei dati non può essere mostrata.")
    else:
        st.info("Generate a dataset to see its summary here.")



# Barra di navigazione
selected = option_menu(
    menu_title=None,
    options=["Generate", "Statistics"],
    icons=["file-earmark-plus", "graph-up"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#333333"},
        "icon": {"color": "#FFFFFF", "font-size": "25px"}, 
        "nav-link": {"font-size": "20px", "text-align": "center", "margin":"0px", "--hover-color": "#00d084"},
        "nav-link-selected": {"background-color": "#00d084"},
    }
)

# Routing basato sulla selezione del menu
if selected == "Generate":
    main_page()
elif selected == "Statistics":
    stats_page()
