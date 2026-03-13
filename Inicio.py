import streamlit as st
import pandas as pd

# ---------------- ENCABEZADO
colA, colB, colC = st.columns([1,6,1])

with colA:
    st.image("logo-club.png", use_column_width=True)

with colC:
    st.image("logo-piad.png", use_column_width=True)

st.header("Bienvenido SPORTING COMPANY!!")
st.write("Videoteca de entrenamientos")

# ---------------- DATA
df_entreno = pd.read_excel("entrenamientos.xlsx")
df_entreno = df_entreno.dropna(subset=["video"])

df_entreno["date"] = pd.to_datetime(df_entreno["date"])

# ---------------- MESES EN ESPAÑOL
meses_map = {
1:"Enero",2:"Febrero",3:"Marzo",4:"Abril",5:"Mayo",6:"Junio",
7:"Julio",8:"Agosto",9:"Septiembre",10:"Octubre",11:"Noviembre",12:"Diciembre"
}

df_entreno["mes_num"] = df_entreno["date"].dt.month
df_entreno["año"] = df_entreno["date"].dt.year

df_entreno["mes_label"] = df_entreno["mes_num"].map(meses_map) + " " + df_entreno["año"].astype(str)

mes = st.sidebar.selectbox(
    "Mes",
    sorted(df_entreno["mes_label"].unique())
)

df_mes = df_entreno[df_entreno["mes_label"] == mes]

# ---------------- SEMANAS COMPLETAS (lunes-domingo)

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

# ---------------- DIAS EN ESPAÑOL

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

dia = st.sidebar.selectbox(
    "Día",
    sorted(df_semana["dia"].unique())
)

df_final = df_semana[df_semana["dia"] == dia]

# ---------------- TITULO FILTRO ACTUAL

st.subheader(f"{mes} • {semana_label} • {dia}")

# ---------------- MOSTRAR VIDEOS

urls_match = df_final["video"].values

n_entreno = df_final.shape[0]
n_columns = 3

for i in range(0, n_entreno, n_columns):

    cols = st.columns(n_columns)

    for j in range(n_columns):

        if i + j < n_entreno:
            cols[j].video(urls_match[i + j], muted=False)