import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from mplsoccer import (VerticalPitch, Pitch, create_transparent_cmap,
                       FontManager, arrowhead_marker, Sbopen)
#from Home_page import name_club, id_club
from etl import df# df_pass
#from functions import barras_apiladas#mapa_pases, passmap_player,player_passmap


import plotly.express as px
from plotly.graph_objs import Scatter
from streamlit_plotly_events import plotly_events
from PIL import Image
#url_powerbi = '<iframe title="Plataforma Dirac v1.1" width="900" height="500" src="https://app.powerbi.com/view?r=eyJrIjoiOWM0YmNkMGEtMzc4Ni00MTI4LTk0OGEtZmFhNzc5NTZiYTkxIiwidCI6IjBlMGNiMDYwLTA5YWQtNDlmNS1hMDA1LTY4YjliNDlhYTFmNiIsImMiOjR9" frameborder="0" allowFullScreen="true"></iframe>'
#st.markdown(url_powerbi, unsafe_allow_html=True)
#----------------------

#st.title(f'⚽ {name_club}')
colX, colY, colZ = st.columns([7, 8, 2])
with colX:st.title('⚽ ANÁLISIS')
with colY:pass
with colZ:st.image('logo-piad.png', use_column_width=True)
#------------ 1. MENU LATERAL
menu_analisis = ['Equipo','Jugadores']
choice = st.sidebar.radio("SUBMENÚ", menu_analisis, 0) #el 0 es el indice de la opcion por defecto
df_players = df.copy()

# ------------------- ANALISIS: EQUIPO ------
if choice == 'Equipo':
    df = df[df.action_type=='colectivo']
    # Barra lateral
    #RIVAL
    rivales = df.Rival.unique()
    n_partido = len(rivales)-1
    menu_match = st.sidebar.selectbox(
        "Partido",
        rivales,
        n_partido)
    #FASE Y TERCIO
    fases = df.Event.unique()
    fases_list = fases.tolist()
    zona = list(df.zone.unique())
    #FASE --OK
    menu_fases = st.sidebar.selectbox(
        "Fase",
        sorted(fases_list),
        0)
    #TERCIO -- OK
    menu_zone = st.sidebar.selectbox(
        "Zona del campo",
        ['Todo']+zona,
        0)


    #FILTRADO DE data
    df = df[df.Rival==menu_match]
    df = df[df.Event==menu_fases]
    
    #Tipo de fase
    tipo_list = df['Tipo'].dropna().unique().tolist()
    #tipo_fase = df.Tipo.unique()
    #tipo_list = tipo_fase.tolist()
    menu_tipo = st.sidebar.selectbox(
        "Tipo",
        ['Todos']+tipo_list,
        0)

    #FILTRADO DATA 2
    if menu_zone == 'Todo':
        pass
    else:
        df = df[df.zone==menu_zone]
    if menu_tipo == 'Todos':
        pass
    else:
        df = df[df.Tipo==menu_tipo]  

# ------ GRAFICOS O TABLA RESUMEN DE DATA

    #st.write(df)
    
# ------ GRAFICANDO CAMPOGRAMA
    fig = px.scatter(
        df, x='x', y='y', #labels={'Nota': 'nota'},
        color='output',
        color_discrete_map={
            'Pérdida': '#AD1D00',
            'Progresión': '#C78B08',
            'Ocasión': '#102C9C',

            'Ocasión rival': '#AD1D00',
            'Progresión riv.':'#FA6019',
            'Recuperación': '#102C9C',
        },
        title=f'{menu_fases} en {menu_match} <br> ➜', hover_data=['time','Nota']
    )
    # Agregar la imagen de fondo al layout
    image = Image.open('campo.png')
    fig.add_layout_image(
        dict(
            source=image,
            xref="x", yref="y",
            x=0,y=0,
            sizex=120,sizey=80,
            sizing="stretch",
            opacity=0.8,
            layer="below",
        )
    )
    # Fijar el tamaño de los ejes
    fig.update_xaxes(range=[0, 120], tickvals=[40,80])
    fig.update_yaxes(range=[80, 0], tickvals=[25,55]) 
    fig.update_layout(
        margin=dict(l=40, r=5, t=50, b=30), # Ajustar los márgenes
        plot_bgcolor='lightgray', #fondo
        paper_bgcolor='lightgray',  # Color de fondo alrededor del gráfico
        hovermode='closest'  # closest' asegura que el punto más cercano al cursor será seleccionado.
    )


    #Mapeo de punto al que se hace clic con el evento (VERIFICAR POR CADA CODIGO)
    #Esto se realiza porque se colocaron varios colores
    #tipo_list = list(df.Tipo.unique())
    #df['CurveN'] = df['Tipo'].apply(lambda x: tipo_list.index(x) if x in tipo_list else -1)
    #df['ptIndx'] = df.groupby('CurveN').cumcount()

    output_list = list(df.output.unique())
    df['CurveN'] = df['output'].apply(lambda x: output_list.index(x) if x in output_list else -1)
    df['ptIndx'] = df.groupby('CurveN').cumcount()
    
    #funcion para extraer el tiempo de inicio y fin de la jugada
    def get_seg(df, curve_value, point_value, get_col):
        result = df.loc[(df['CurveN'] == curve_value) & (df['ptIndx'] == point_value), get_col]
        return result.iloc[0] if not result.empty else None 

    # Capturar el clic del usuario en el gráfico
    selected_points = plotly_events(fig, click_event=True, hover_event=False)
    #st.write(selected_points)
    
    # Si se ha seleccionado un punto, mostrar el video asociado
    df = df.reset_index(drop=True)
    if selected_points:
        #st.write(selected_points)
        point_idx = selected_points[0]['pointIndex']
        video_url = df.at[point_idx, 'Video'] #cuidado aqui, si hay dos fuente de video no funcionará
        curve_n = selected_points[0]['curveNumber']
        #st.write(curve_n)
        start_time = get_seg(df, curve_n, point_idx,'seg_start')
        #st.write(start_time)
        end_time = get_seg(df, curve_n, point_idx,'seg_end')
        #st.write(end_time)
        st.video(video_url, start_time=start_time, end_time=end_time, loop=0, muted=0)

# ----------- ANALISIS: JUGADORES -------------------------------------
elif choice == 'Jugadores':

    df_ind = df_players[df_players.action_type=='individual']

    # Barra lateral
    #RIVAL
    rivales = df_ind.Rival.unique()
    n_partido = len(rivales)-1
    menu_match = st.sidebar.selectbox(
        "Partido",
        rivales,
        n_partido)
    #Jugador Y TERCIO
    players = df_ind.player.unique()
    players_list = players.tolist()
    zona = list(df_ind.zone.unique())
    #Jugadores --OK
    menu_players = st.sidebar.selectbox(
        "Jugadores",
        players_list,
        0)
    #TERCIO -- OK
    menu_zone = st.sidebar.selectbox(
        "Zona del campo",
        ['Todo']+zona,
        0)
    #FILTRADO DE data
    df_ind = df_ind[df_ind.Rival==menu_match]
    df_ind = df_ind[df_ind.player==menu_players]
    if menu_zone == 'Todo':
        pass
    else:
        df_ind = df_ind[df_ind.zone==menu_zone]

    #------------ CAMPOGRAMA-------------------------------------------

    fig = px.scatter(
        df_ind, x='x', y='y', #labels={'Nota': 'nota'},
        color='Event',
        color_discrete_map={
            'PERDIDA': '#AD1D00',
            'REGATE': "#7108C7",
            'TIRO': '#102C9C',

            'PASE': 'black',
            'CONDUCCION':'#FA6019',
        },
        hover_data={
            'x': False,
            'y': False,
            'output':True,
            'time': True,
            'Nota': True
        },
        title=f'{menu_players} vs {menu_match} <br> ➜', #hover_data=['time','Nota']
    )
    # Agregar la imagen de fondo al layout
    image = Image.open('campo.png')
    fig.add_layout_image(
        dict(
            source=image,
            xref="x", yref="y",
            x=0,y=0,
            sizex=120,sizey=80,
            sizing="stretch",
            opacity=0.8,
            layer="below",
        )
    )
    # Fijar el tamaño de los ejes
    fig.update_xaxes(range=[0, 120], tickvals=[40,80])
    fig.update_yaxes(range=[80, 0], tickvals=[25,55]) 
    fig.update_layout(
        margin=dict(l=40, r=5, t=50, b=30), # Ajustar los márgenes
        plot_bgcolor='lightgray', #fondo
        paper_bgcolor='lightgray',  # Color de fondo alrededor del gráfico
        hovermode='closest'  # closest' asegura que el punto más cercano al cursor será seleccionado.
    )


    #Mapeo de punto al que se hace clic con el evento (VERIFICAR POR CADA CODIGO)
    #Esto se realiza porque se colocaron varios colores
    #tipo_list = list(df.Tipo.unique())
    #df['CurveN'] = df['Tipo'].apply(lambda x: tipo_list.index(x) if x in tipo_list else -1)
    #df['ptIndx'] = df.groupby('CurveN').cumcount()

    acctions_list = list(df_ind.Event.unique())
    df_ind['CurveN'] = df_ind['Event'].apply(lambda x: acctions_list.index(x) if x in acctions_list else -1)
    df_ind['ptIndx'] = df_ind.groupby('CurveN').cumcount()
    
    #funcion para extraer el tiempo de inicio y fin de la jugada
    def get_seg(df, curve_value, point_value, get_col):
        result = df.loc[(df['CurveN'] == curve_value) & (df['ptIndx'] == point_value), get_col]
        return result.iloc[0] if not result.empty else None 

    # Capturar el clic del usuario en el gráfico
    selected_points = plotly_events(fig, click_event=True, hover_event=False)
    #st.write(selected_points)
    
    # Si se ha seleccionado un punto, mostrar el video asociado
    df_ind = df_ind.reset_index(drop=True)
    if selected_points:
        #st.write(selected_points)
        point_idx = selected_points[0]['pointIndex']
        video_url = df_ind.at[point_idx, 'Video'] #cuidado aqui, si hay dos fuente de video no funcionará
        curve_n = selected_points[0]['curveNumber']
        #st.write(curve_n)
        start_time = get_seg(df_ind, curve_n, point_idx,'seg_start')
        #st.write(start_time)
        end_time = get_seg(df_ind, curve_n, point_idx,'seg_end')
        #st.write(end_time)
        st.video(video_url, start_time=start_time, end_time=end_time, loop=0, muted=0)