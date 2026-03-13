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
df_entreno = pd.read_excel('Entrenamientos.xlsx')


#FORMATO
st.header(f'Bienvenido SPORTING COMPANY!!')

st.write("Videoteca: Partidos & Entrenamientos")

df_entreno = df_entreno.dropna(subset=['video'])

#-----------FILTRO POR FECHA
df_entreno['date'] = pd.to_datetime(df_entreno['date'])
# MES
meses = df_entreno['date'].dt.to_period('M').unique()
mes = st.sidebar.selectbox("Mes", meses)
df_mes = df_entreno[df_entreno['date'].dt.to_period('M') == mes]
# SEMANA
semanas = df_mes['date'].dt.isocalendar().week.unique()
semana = st.sidebar.selectbox("Semana", semanas)
df_semana = df_mes[df_mes['date'].dt.isocalendar().week == semana]
# DIA
dias = df_semana['date'].dt.day_name().unique()
dia = st.sidebar.selectbox("Día", dias)
df_final = df_semana[df_semana['date'].dt.day_name() == dia]

#######-------------

'''
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
'''
urls_match = df_entreno['video'].values

#df_matches = df_matches[df_matches['match_filter'].isin(partidos_select)]
n_matches = df_entreno.shape[0]
n_columns = 3
for i in range(0, n_matches, n_columns):
    cols = st.columns(n_columns)
    for j in range(n_columns):
        if i + j < n_matches:
            cols[j].video(urls_match[i + j], muted=0)