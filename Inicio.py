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

# -------- FECHAS
df_entreno['date'] = pd.to_datetime(df_entreno['date'])

# calcular lunes de cada semana
df_entreno["week_start"] = df_entreno["date"] - pd.to_timedelta(df_entreno["date"].dt.weekday, unit="d")

# calcular domingo
df_entreno["week_end"] = df_entreno["week_start"] + pd.Timedelta(days=6)

# crear etiqueta visual
df_entreno["week_label"] = df_entreno["week_start"].dt.strftime(
    "Semana (%d %b"
) + " - " + df_entreno["week_end"].dt.strftime("%d %b %Y)")

# semanas disponibles
semanas = sorted(df_entreno["week_start"].unique())

# crear labels para selector
labels = {
    start: f"Semana ({start.day}-{(start + pd.Timedelta(days=6)).day} {start.strftime('%B')})"
    for start in semanas
}

semana_seleccionada = st.sidebar.selectbox(
    "Semana de trabajo",
    list(labels.keys()),
    format_func=lambda x: labels[x]
)

inicio_semana = semana_seleccionada
fin_semana = inicio_semana + pd.Timedelta(days=6)

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