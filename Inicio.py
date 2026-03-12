import streamlit as st
import numpy as np
import pandas as pd

#st.set_page_config(layout="wide")

# ENCABEZADO: escudo Melgar + escudo Liga1
colA, colB, colC = st.columns([1, 7, 1])
with colA:
    st.image('logo-club.png', use_column_width=True)
with colB:
    pass
with colC:
    st.image('logo-piad.png', use_column_width=True)
    pass

#DATA
df_matches = pd.read_excel('Matches.xlsx')


#FORMATO
st.header(f'Bienvenido TOTO Camargo!!')

st.write("Videoteca: Partidos completos")

df_matches = df_matches.dropna(subset=['video'])
df_matches = df_matches[df_matches.Propio==True]
#rivales = df_matches['match_filter'].values
etapa = set(df_matches['Etapa'].values)

etapa_select = st.sidebar.multiselect(
    "Elige la etapa",
    etapa,
    etapa)
#partidos_select = st.sidebar.multiselect(
#    "Elige el rival",
#    rivales,
#    rivales)
df_matches = df_matches[df_matches['Etapa'].isin(etapa_select)]
urls_match = df_matches['video'].values

#df_matches = df_matches[df_matches['match_filter'].isin(partidos_select)]
n_matches = df_matches.shape[0]
n_columns = 3
for i in range(0, n_matches, n_columns):
    cols = st.columns(n_columns)
    for j in range(n_columns):
        if i + j < n_matches:
            cols[j].video(urls_match[i + j], muted=0)