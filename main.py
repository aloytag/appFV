# -*- coding: utf-8 -*-

import os
import io
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from auxiliares import clk_btn

if 'N' not in st.session_state:
    st.session_state['N'] = 125

with st.sidebar:
    st.write('### Parámetros')
    N = st.slider('Cantidad de paneles', min_value=1,
                  max_value=1000, step=1, key='N')
    Ppico = st.number_input('Pot. pico del panel (W)', min_value=0,
                             max_value=500, value=240, step=10)
    kp = st.number_input('Coef. de pot.-temp. (1/°C)', min_value=-0.01,
                         max_value=0., value=-0.0044, step=0.0001,
                         format='%.4f')
    eta = st.number_input('Rendimiento general (p.u.)', min_value=0.1,
                          max_value=1., value=0.97, step=0.01,
                          format='%.2f')
    

tab1, tab2 = st.tabs(['Generación FV', 'Pestaña 2'])
with tab2:
    st.title('Título')
    st.write('## Subtítulo')
    st.write('### Sub-Subtítulo')

    """
    asfdferreg
    ergege

    **fererf**

    1. efewfwe
    2. effref
    3. ffefef

    $ I = \int\limits_{a=1}^{b=7} f(x) \cdot dx $

    $ \left[ \\begin{array}{cc}
    4 & 5 \\\\
    6 & 11 \end{array} \\right] $
    """

    btn = st.button('Hacer click', on_click=clk_btn)

with tab1:
    with open('texto.md', 'r') as arch:
        txt = arch.read()
        st.write(txt)

    col1, col2, col3 = st.columns(3, gap='large')
    with col1:
        G = st.number_input('Irradiancia (W/m2)', min_value=0, max_value=2000,
                            value=1000)
    with col2:
        Tc = st.number_input('Temp. celda (°C)', min_value=-20., max_value=60.,
                            value=25., step=1., format='%.1f')
    with col3:
        btn_calP = st.button('Calcular')
    
    if btn_calP:
        p = N * G/1000 * Ppico * (1 + kp * (Tc - 25)) * eta * 1e-3  # kW
        st.info(f'La potencia obtenida es {p: .2f} (kW)')
    else:
        st.warning('Click en el botón para calcular')
    

    arch_cargado = st.file_uploader('Subir datos', type='xlsx',
                            accept_multiple_files=False)
    if arch_cargado is not None:
        tabla = pd.read_excel(arch_cargado, index_col=0)
        tabla['Potencia (kW)'] = N * tabla['Irradiancia (W/m²)']/1000 * Ppico * (1 + kp * (tabla['Temperatura (°C)'] - 25)) * eta * 1e-3  # kW
        tabla_mayo = tabla.loc['2019-5', :]
        st.dataframe(tabla)

        st.line_chart(tabla_mayo, y='Potencia (kW)')

        archivo_ram = io.BytesIO()
        f, ax = plt.subplots(figsize=(8, 4))
        tabla_mayo.plot.line(y='Temperatura (°C)', ax=ax)
        ax.grid()
        f.savefig(archivo_ram, format='png', dpi=150)
        st.image(archivo_ram)
    else:
        st.warning('Resta cargar archivo de datos', icon='⚠️')
        
    if arch_cargado is not None:
        archivo_ram_tabla = io.BytesIO()
        tabla.to_excel(archivo_ram_tabla)
        st.download_button('Decargar resultados', data=archivo_ram_tabla,
                           file_name='Resultados.xlsx')
