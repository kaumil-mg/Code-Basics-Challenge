import pandas as pd
import streamlit as st
import pygwalker as pyg
import warnings
from pygwalker.api.streamlit import StreamlitRenderer

warnings.filterwarnings('ignore')

st.set_page_config(page_title='Free Data Visualization', page_icon=':smile:', layout='wide')

st.title(':bar_chart: Welcome to Free Visualization Platform')
st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)

f1 = st.file_uploader(':file_folder: Upload your file', type=['csv', 'txt', 'xlsx'])

if f1 is not None:
    filename = f1.name
    st.write(f"Filename: {filename}")
    
    # Read the file into a DataFrame
    if filename.endswith('.csv'):
        df = pd.read_csv(f1)
    elif filename.endswith('.txt'):
        df = pd.read_csv(f1, delimiter='\t')  # Assuming tab-delimited for TXT files
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(f1)
    else:
        st.error('Unsupported file type')
        df = None
    
    if df is not None:
        st.write(df.head())  # Display the first few rows of the dataframe
        
        # Pass the DataFrame to StreamlitRenderer
        pyg_app = StreamlitRenderer(df)
        pyg_app.explorer()
else:
    st.write('Upload your file')
