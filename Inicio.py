import streamlit as st
import pandas as pd

# ---------------- ENCABEZADO
colA, colB, colC = st.columns([1,6,1])

with colA:
    st.image("logo-club.png", use_column_width=True)

with colC:
    st.image("logo-piad.png", use_column_width=True)

st.header("Bienvenido SPORTING COMPANY!!")
#st.write("Videoteca de entrenamientos")

# ---------------- DATA
df_entreno = pd.read_excel("entrenamientos.xlsx")
# SOLO registros con video
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

# -------- seleccionar semana actual por defecto

hoy = pd.Timestamp.today()
labels = list(semanas_dict.keys())
index_default = 0
for idx, (ini, fin) in enumerate(semanas_dict.values()):
    if ini <= hoy <= fin:
        index_default = idx
        break
semana_label = st.sidebar.selectbox(
    "Semana",
    labels,
    index=index_default
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

df_semana["dia_en"] = df_semana["date"].dt.day_name()
df_semana["dia"] = df_semana["dia_en"].map(dias_map)

df_semana["dia_label"] = df_semana["dia"] + " " + df_semana["date"].dt.strftime("%d %b")

# ordenar por fecha más reciente
dias_ordenados = (
    df_semana.sort_values("date", ascending=False)
    .drop_duplicates("dia_label")["dia_label"]
)

dia = st.sidebar.selectbox(
    "Día",
    dias_ordenados,
    index=0
)

df_final = df_semana[df_semana["dia_label"] == dia]


# ---------------- TITULO ACTUAL

#st.write(f"{semana_label} -> {dia}")

st.write(f"**:green[{semana_label} -> {dia}]**")

# ---------------- VIDEOS

# Extraemos los datos necesarios
urls_match = df_final["video"].values
coments_entreno = df_final["comentarios"].values
nombres = df_final["Nombre"].values  # Asegúrate de tener esta columna
n_entreno = df_final.shape[0]

for i in range(n_entreno):
    # 1. Mostramos el nombre ocupando todo el ancho
    #st.subheader(nombres[i])
    st.markdown(f"#### {nombres[i]}")

    # 2. Creamos dos columnas: una para el video principal y otra para el contenido
    # Puedes ajustar el ratio [2, 1] si quieres que el video sea más grande que el texto
    col_video, col_comentario = st.columns([3, 4])

    with col_video:
        st.video(urls_match[i], muted=False)

    with col_comentario:
        comentario = coments_entreno[i]
        
        if pd.notna(comentario):
            comentario = str(comentario)
            
            # Si el comentario es un link de video
            if "youtu" in comentario:
                st.video(comentario, muted=False)
            # Si es texto normal
            else:
                st.info(comentario) # Usar .info() le da un mejor estilo visual al texto

    st.divider()