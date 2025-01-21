import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()
from aux_img import img_1, img_2, img_3, img_4, img_5
from aux_preprocesado import preprocesado, preprocesado_columnas, bases_de_datos, procesar_datos_v,preprocesar_df_est, calcular_prol_vivo
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
    st.markdown('<div class="titulo"><b>ANÁLISIS IN VITRO</b></div>', unsafe_allow_html=True)

    _,c1,c2,_ = st.columns([0.3, 1.5,4,0.3], gap = 'large')

    with c1:
        st.header('Carga de datos')
        uploaded_file = st.file_uploader("Introduce fichero análisis in vitro")
        if uploaded_file is not None:
            # Cargar los datos y mostrarlos
            df = pd.read_csv(uploaded_file, sep = ';')
            st.write(df)
            # preprocesado
            c_met, c_lnp, c_dia, c_id = preprocesado_columnas(df)
            resumen_series, df0 = preprocesado(df)
            l_lnp = df.loc[~df[c_lnp].isna(),c_lnp].unique()
            sol = bases_de_datos(resumen_series, df0, l_lnp)
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
            l_lnp_pdf = st.multiselect("Seleccionar línea celular",l_lnp)
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
        st.header('Seleccionar línea celular')
        lnp = c2.selectbox('',l_lnp)
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
                st.write(sol['df_dif_perc_' + lnp].transpose().round(2))


with st.container():
    
    st.markdown('<div class="titulo"><b>ANÁLISIS IN VIVO</b></div>', unsafe_allow_html=True)
    _,c1_vv,c2_vv,_ = st.columns([0.3, 1.5,4,0.3], gap = 'large')
    with c1_vv:
        st.header('Carga de datos')
        uploaded_file_vv = st.file_uploader("Introduce fichero análisis in vivo")
        if uploaded_file_vv is not None:
            # Cargar los datos y mostrarlos
            df_vv = pd.read_csv(uploaded_file_vv, sep = ';')
            st.write(df_vv)
            #
            # Preprocesado
            col_met,col_id ,col_dia,col_v1 ,col_v2 ,col_v3 = df_vv.columns
            df_vv[col_id] = df_vv[col_met] + '_' + df_vv[col_id]
            for col in [col_v1, col_v2, col_v3]:df_vv[col] = [np.nan if pd.isna(el) else float(el.replace(',','.')) for el in df_vv[col]]
            df_v1 = procesar_datos_v(df_vv, col_v1, col_id, col_dia)
            df_v2 = procesar_datos_v(df_vv, col_v2, col_id, col_dia)
            df_v3 = procesar_datos_v(df_vv, col_v3, col_id, col_dia)
            df_vol = df_v1 * df_v2 * df_v3
            # Img a mostrar
            fig3, ax3 = plt.subplots(figsize = (12,3), ncols = 3)
            img_3(ax3,df_v1, df_v2, df_v3, bigotes = True)
            fig4, ax4 = plt.subplots(figsize = (6,3))
            img_4(ax4,df_vol, bigotes= True)
            fig5, ax5 = plt.subplots(figsize = (6,3))
            img_5(ax5, df_vol)
            
            # Img para el pdf
            dict_fig_pdf_vv = {}
            dict_fig_pdf_vv[3], ax3_pdf = plt.subplots(figsize = (8,3), ncols = 3)
            img_3(ax3_pdf,df_v1, df_v2, df_v3, bigotes = True)
            dict_fig_pdf_vv[4], ax4_pdf = plt.subplots(figsize = (8,3))
            img_4(ax4_pdf,df_vol, bigotes= True)
            dict_fig_pdf_vv[5], ax5_pdf = plt.subplots(figsize = (8,3))
            img_5(ax5_pdf, df_vol)
    with c2_vv:
        if uploaded_file_vv is not None:
            c2_vv.subheader('Resultados')
            c2_vv.subheader('Gráficas')
            st.pyplot(fig = fig3)
            c21_vv,c22_vv = st.columns(2)
            with c21_vv:st.pyplot(fig = fig4)
            with c22_vv:st.pyplot(fig = fig5)
            df_T = pd.concat([preprocesar_df_est(df_aux,'Tratamiento')['Tratamiento_mean'] for df_aux in [df_v1, df_v2, df_v3, df_vol]] + [calcular_prol_vivo(df_vol) ], axis = 1)
            df_T.columns = [col_v1, col_v2, col_v3, 'Volume', 'Proliferation']
            df_C = pd.concat([preprocesar_df_est(df_aux,'Control')['Control_mean'] for df_aux in [df_v1, df_v2, df_v3, df_vol]] + [calcular_prol_vivo(df_vol)*0 + 100], axis = 1)
            df_C.columns = [col_v1, col_v2, col_v3, 'Volume', 'Proliferation']
            with c21_vv:
                st.subheader('Resumen tratamiento')
                st.write(df_T)
            with c22_vv:
                st.subheader('Resumen Control')
                st.write(df_C)
            



