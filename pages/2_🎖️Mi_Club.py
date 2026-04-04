import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from mplsoccer import (VerticalPitch, Pitch, create_transparent_cmap,
                       FontManager, arrowhead_marker, Sbopen)

#from Home_page import name_club, id_club
from etl import df #df_pass #df_tipo1, df_tipo2
from functions import barras_apiladas, tipo_tiros_goles, mostrar_tablas_zonas, mapa_pases


colA, colB, colC = st.columns([5, 6, 2])
with colA:st.title('🎖️ MI CLUB')
with colB:pass
with colC:st.image('logo-piad.png', use_column_width=True)
#----------------------
#st.title(f'⚽ {name_club}')
#df = df[df['etapa'] != 'provincial'] #estamos obviando los partidos de la provincial


#ETAPA DE JUEGO
ataque = ['Ataque', 'Tran. Defensa-Ataque']
defensa= ['Defensa', 'Tran. Ataque-Defensa']

#------------ 1. MENU LATERAL
menu_miclub = ['Informe de partido','Informe acumulado']
choice2 = st.sidebar.radio("Submenú - Miclub", menu_miclub, 0)

if choice2 == 'Informe de partido':

    # Barra lateral
    #RIVAL
    rivales = df.Rival.unique()
    n_partido = len(rivales)-1
    menu_match = st.sidebar.selectbox(
        "Partido",
        rivales,
        n_partido)
    df = df[df.Rival==menu_match]

    etapas_juego = ['Ataque', 'Defensa']#,'Pases']

    #menu_subinforme = st.sidebar.selectbox(
    #    "Etapa de juego",
    #    etapas_juego,
    #    0)
    st.markdown(
    """
    <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; border-left: 5px solid #ff4b4b;">
        <h3 style="margin: 0; color: #31333F; font-family: sans-serif;">
            ATAQUE & TRAN. OFENSIVA
        </h3>
    </div>
    <br>
    """,
    unsafe_allow_html=True
)

    #if menu_subinforme == 'Ataque':
    col1, col2 = st.columns(2)
    with col1:
        #st.subheader("Gráfico Ataque")
        #fig1, ax1 = plt.subplots()
        #ax1.plot([1, 2, 3], [10, 20, 10])
        barras_apiladas(df, 'Event', ataque,'output', "¿Cómo terminó la jugada con balón?")
    with col2:
        tipo_tiros_goles(df,'Ocasión')
        #mostrar_tablas_zonas(df, ataque)


    st.markdown(
    """
    <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; border-left: 5px solid #ff4b4b;">
        <h3 style="margin: 0; color: #31333F; font-family: sans-serif;">
            DEFENSA & TRAN. DEFENSIVA
        </h3>
    </div>
    <br>
    """,
    unsafe_allow_html=True
    )
    #if menu_subinforme == 'Defensa':
    col1, col2 = st.columns(2)
    with col1:
        #st.subheader("Gráfico Ataque")
        #fig1, ax1 = plt.subplots()
        #ax1.plot([1, 2, 3], [10, 20, 10])
        barras_apiladas(df, 'Event', defensa,'output', "¿Cómo terminó la jugada Defensiva?")
    with col2:
        tipo_tiros_goles(df,'Ocasión rival')
        #mostrar_tablas_zonas(df, defensa)
    
        

if choice2 == 'Informe acumulado':
    st.write("NO DISPONIBLE")