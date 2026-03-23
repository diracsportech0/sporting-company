import streamlit as st
import numpy as np
import pandas as pd
from etl import df, df_pass
from functions import player_passmap,graph_barras, heat_map

#----------------------
df_players_excel = pd.read_excel('players.xlsx')

#OBTENER DATA TOTALIZADA POR JUGADOR
# Agrupar por Partido, Jugador y Evento y contar ocurrencias
grouped = df.groupby(['Rival', 'player', 'Event']).size().reset_index(name='count')
# Pivotar los datos para transformar los eventos en columnas
pivot_table = grouped.pivot_table(index=['Rival', 'player'], columns='Event', values='count', fill_value=0)
# Restablecer el índice para que Partido y Jugador sean columnas nuevamente
df_players_totalstats = pivot_table.reset_index()

#MENU LATERAL
players = set(df_players_totalstats['player'].values)
player = st.sidebar.selectbox(
        "Jugador",
        players,
        0)
df_player = df_players_totalstats[df_players_totalstats.player==player]
n_partidos = df_player.shape[0] #partidos jugados por un futbolista

st.title("🚹 MI PLANTEL")
#--- CONTENIDO INFO BASICA
matching_row = df_players_excel.loc[df_players_excel['player'] == player]
name_player = matching_row['name_complete'].values[0]
apellido = matching_row['surname'].values[0]

#born_player = matching_row['born'].values[0].astype('M8[ms]').astype('O').strftime('%Y/%m/%d')
#min_played = matching_row['min_played'].values[0]
dorsal= matching_row['dorsal'].values[0]
#edad_player = matching_row['edad'].values[0]


# TABLA
df_events_player = df[df.player==player]
metric_off = ['CONDUCCION','PASE','REGATE','TIRO']
metric_def = ['INTERCEPTACION','DUELO', 'DESPEJE','RECUPERACION',
              'PRESION']
#
colA3, colB3, colC3, colD3, colE3= st.columns([3,3,2,5,1])
try:
        with colA3:st.image(f'imgs/{apellido}.jpg', use_column_width=True)
except:
      with colA3:st.image('imgs/perfil.jfif', use_column_width=True)
with colB3:
         st.write('Jugador:', name_player)
         st.write('Posición:', matching_row['position'].values[0])
#        st.write('Nacimiento:', born_player)
         #st.write('Edad:', edad_player)
         st.write('Partidos jugados:', n_partidos)
         st.write('Dorsal:', dorsal)
with colC3: pass
with colE3: pass

colA4, colB4 = st.columns([1,1])
with colA4: option_stats = st.selectbox("Estadísticas",("Con balón", "Sin balón"))
with colB4: pass

if option_stats == 'Con balón':
        metrics_select = metric_off
        player_metr_sel = df_player[metrics_select]
        with colD3: heat_map(df_events_player,metrics_select)
        #player_table1 = {'player':None,
        #                'Corner':None, 'Despeje':None, 'Duelo defensivo':None, 'Falta cometida':None,
        #                'Interceptación':None, 'Presión':None, 'Duelo ofensivo':None,'Duelo aereo':None,
        #                'Recuperacion':None}
        #st.dataframe(df_player, column_config=player_table1)
        st.write(player_metr_sel)

elif option_stats == 'Sin balón':
        metrics_select = metric_def
        player_metr_sel = df_player[metrics_select]
        with colD3: heat_map(df_events_player,metrics_select)
        #player_table2 = {'player':None,
        #                'Carrera':None, 'Corner':None, 'Falta recibida':None, 'Off-side':None,
        #                'Pase':None, 'Regate':None, 'Tiro arco':None, 'Tiro desviado':None,
        #                'Tiro bloqueado':None, 'Tiro libre':None, 'Otras perdidas':None,
        #                'Duelo ofensivo':None}
        #st.dataframe(df_player, column_config=player_table2)
        st.write(player_metr_sel)

######## --------------- MAPA DE PASES
df_pass_player = df_pass[df_pass.player==player]
#df_pass_player = df_pass_player[df_pass_player.match_filter==rival]
player_passmap(df_pass_player,player,'ADEPA')

'''
metricas = ['PASE','CONDUCCION','REGATE','TIRO','PERDIDA',
            'PRESION','DUELO',
            'INTERCEPTACION','DESPEJE', 'RECUPERACION']
heat_map(df_player, metricas)
'''


