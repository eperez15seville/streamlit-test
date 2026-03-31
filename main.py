import streamlit as st
import pandas as pd
import numpy as np
import math
import random

st.write('Mi primera aplicación!')

st.subheader('Carga de datos')

from ucimlrepo import fetch_ucirepo 

@st.cache_resource
def load_wine_data():
    """Carga el dataset de calidad del vino (se ejecuta solo una vez)"""
    wine_quality = fetch_ucirepo(id=186)
    return wine_quality

with st.spinner('Cargando el conjunto de datos de calidad del vino...'):
    wine_quality = load_wine_data()
    
    # data (as pandas dataframes) 
    X = wine_quality.data.features 
    y = wine_quality.data.targets 

st.success('Datos cargados exitosamente!')

st.subheader('Gráficos')

import plotly.express as px
fig = px.pie(wine_quality.variables, names='type', title='Distribución de Tipos de Variables')

st.plotly_chart(fig)

st.subheader('Tablas')

continuous_vars = wine_quality.variables[wine_quality.variables['type'] == 'Continuous']
st.dataframe(continuous_vars)

st.subheader('Selector y actualización de gráficos')

selected_var = st.selectbox('Selecciona una variable continua:', continuous_vars['name'])
fig = px.box(X, y=selected_var, title=f'Boxplot de {selected_var}')
st.plotly_chart(fig)

st.subheader('Otros gráficos')

fig = px.pie(wine_quality.data.original, names='color', title='Distribución de Colores de Vino')
st.plotly_chart(fig)

import plotly.graph_objects as go

correlacion = X.select_dtypes(include=['float64', 'int64']).corr()

fig = go.Figure(data=go.Heatmap(
    z=correlacion.values,
    x=correlacion.columns,
    y=correlacion.columns,
    colorscale='RdBu',
    zmid=0))

fig.update_layout(title='Matriz de Correlación',
                  xaxis_title='Variables',
                  yaxis_title='Variables')

st.plotly_chart(fig)

st.subheader('Mapa')

sevilla_map_data = pd.DataFrame({
    'lat': [37.3604728],
    'lon': [-5.9914384]
})

st.map(sevilla_map_data, zoom=16)
