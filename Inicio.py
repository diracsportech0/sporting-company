import streamlit as st
import numpy as np
import pandas as pd

# ENCABEZADO
colA, colB, colC = st.columns([1, 6, 1])
with colA:
    st.image('logo-club.png', use_column_width=True)
with colC:
    st.image('logo-piad.png', use_column_width=True)

# DATA
df_entreno = pd.read_excel('entrenamientos.xlsx')

st.header('Bienvenido SPORTING COMPANY!!')
st.write("Videoteca de entrenamientos")

df_entreno = df_entreno.dropna(subset=['video'])

# -------- FECHAS-----
df_entreno['date'] = pd.to_datetime(df_entreno['date'])

# -------- SEMANAS COMPLETAS DEL MES (lunes-domingo)

mes_num = df_mes["date"].dt.month.iloc[0]
anio = df_mes["date"].dt.year.iloc[0]

primer_dia = pd.Timestamp(anio, mes_num, 1)
ultimo_dia = primer_dia + pd.offsets.MonthEnd()

# lunes anterior al primer día del mes
inicio = primer_dia - pd.Timedelta(days=primer_dia.weekday())

semanas_dict = {}
i = 1

while inicio <= ultimo_dia:

    fin = inicio + pd.Timedelta(days=6)

    label = f"Semana {i} ({inicio.strftime('%d %b')} - {fin.strftime('%d %b')})"

    semanas_dict[label] = (inicio, fin)

    inicio += pd.Timedelta(days=7)
    i += 1


semana_label = st.sidebar.selectbox(
    "Semana",
    list(semanas_dict.keys())
)

inicio_semana, fin_semana = semanas_dict[semana_label]

df_semana = df_entreno[
    (df_entreno["date"] >= inicio_semana) &
    (df_entreno["date"] <= fin_semana)
]

# ---------- DIAS EN ESPAÑOL
dias_map = {
    "Monday":"Lunes",
    "Tuesday":"Martes",
    "Wednesday":"Miércoles",
    "Thursday":"Jueves",
    "Friday":"Viernes",
    "Saturday":"Sábado",
    "Sunday":"Domingo"
}

df_semana["dia"] = df_semana["date"].dt.day_name().map(dias_map)

dia = st.sidebar.selectbox("Día", df_semana["dia"].unique())

df_final = df_semana[df_semana["dia"] == dia]

# -------- MOSTRAR VIDEOS FILTRADOS
urls_match = df_final['video'].values

n_entreno = df_final.shape[0]
n_columns = 3

for i in range(0, n_entreno, n_columns):
    cols = st.columns(n_columns)
    for j in range(n_columns):
        if i + j < n_entreno:
            cols[j].video(urls_match[i + j], muted=0)