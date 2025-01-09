import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()
from aux_img import img_1, img_2
from aux_preprocesado import preprocesado, preprocesado_columnas, bases_de_datos
from aux_html import escribir_html
st.set_page_config(page_title="Análisis eficiencia", layout="wide")
import os
from pathlib import Path
img_file = 'Img'
path = Path("Img")
if not path.exists():
    os.makedirs(path)
#
st.markdown("""
    <style>
        .titulo {
            background-color: #709acd;
            padding: 10px;
            border-radius: 5px;color:#ffffff; font-size: 80px;text-align: center;
        }
    </style>
""", unsafe_allow_html=True)
    

#
with st.container():
    st.markdown('<div class="titulo"><b>ANÁLISIS DE EFICIENCIA</b></div>', unsafe_allow_html=True)

    _,c1,c2,_ = st.columns([0.3, 1.5,4,0.3], gap = 'large')

    with c1:
        st.header('Carga de datos')
        uploaded_file = st.file_uploader("Introduce fichero")
        if uploaded_file is not None:
            # Cargar los datos y mostrarlos
            df = pd.read_csv(uploaded_file, sep = ';')
            st.write(df)
            # preprocesado
            c_met, c_lnp, c_dia, c_id = preprocesado_columnas(df)
            resumen_series, df0 = preprocesado(df)
            sol = bases_de_datos(resumen_series, df0)
            l_lnp = df.loc[~df[c_lnp].isna(),c_lnp].unique()
            # Crear todas las imágenes
            dict_fig = {}
            for lnp in l_lnp:
                fig1, ax = plt.subplots(figsize = (8,3), ncols = 2)
                img_1(fig1, ax, sol, df0, lnp,img_file)
                fig2, ax2 = plt.subplots(figsize = (8,3))
                img_2(fig2, ax2, sol, lnp,img_file)
                dict_fig[lnp] = {1:fig1, 2:fig2}
            dict_fig_pdf = {}
            for lnp in l_lnp:
                fig1, ax = plt.subplots(figsize = (10, 3), ncols = 2)
                img_1(fig1, ax, sol, df0, lnp,img_file)
                fig2, ax2 = plt.subplots(figsize = (10, 3))
                img_2(fig2, ax2, sol, lnp,img_file)
                dict_fig_pdf[lnp] = {1:fig1, 2:fig2}
            
            # Numero de para la descarga
            st.header('Descarga')
            l_lnp_pdf = st.multiselect("LNP Informe",l_lnp)
            escribir_html(sol, img_file, l_lnp_pdf)
            if l_lnp_pdf != []:
                # Boton descarga pdf
                with open("example.pdf", "rb") as pdf_file:
                    PDFbyte = pdf_file.read()
                st.download_button(label="Resultados",
                                    data=PDFbyte,
                                    file_name="resultados.pdf",
                                    mime='application/octet-stream')
        else: l_lnp = []


    with c2:
        st.header('LNP a mostrar')
        lnp = c2.selectbox('Selecciona LNP',l_lnp)
        if uploaded_file is not None and lnp is not None:
            c2.subheader('Resultados ' + lnp)
            c21, c22 = st.columns([2,1], gap = 'large')
            with c21:
                c21.subheader('Gráficas')
                st.pyplot(fig = dict_fig[lnp][1])
                st.pyplot(fig = dict_fig[lnp][2])


            with c22:
                c22.subheader('Tablas')
                st.write('VALORES MEDIOS')
                st.write(sol['df_medios_' + lnp].transpose())
                st.write('VALORES MEDIOS DIFERENCIADOS')
                st.write(sol['df_dif_' + lnp].transpose())
                st.write('PROLIFERACIÓN')
                st.write(sol['df_dif_perc_' + lnp].transpose())


with st.container():
    
    st.markdown('<div class="titulo"><b>ANÁLISIS DE TOXICIDAD</b></div>', unsafe_allow_html=True)
