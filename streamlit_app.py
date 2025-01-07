import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()
from aux_img import img_1, img_2
from aux_preprocesado import preprocesado, preprocesado_columnas, bases_de_datos
st.set_page_config(page_title="Análisis eficiencia", layout="wide")




c1,c2 = st.columns([ 1.5,4], gap = 'large')

with c1:
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, sep = ';')
        st.write(df)

        img_file = '/workspaces/gdp-dashboard/Img'

        c_met, c_lnp, c_dia, c_id = preprocesado_columnas(df)
        resumen_series, df0 = preprocesado(df)
        sol = bases_de_datos(resumen_series, df0)
        #
        l_lnp = df.loc[~df[c_lnp].isna(),c_lnp].unique()
        lnp_ef = c1.selectbox('Selecciona LNP',l_lnp)


with c2:
    if uploaded_file is not None and lnp_ef is not None:
        c2.title('Resultados ' + lnp_ef)
        c21, c22 = st.columns([2,1], gap = 'large')
        with c21:
            c21.title('Gráficas')
            fig, ax = plt.subplots(figsize = (8,2.5), ncols = 2)
            img_1(fig, ax, sol, df0, lnp_ef,img_file)
            st.pyplot(fig = fig)
            fig2, ax2 = plt.subplots(figsize = (8,2.5))
            img_2(fig2, ax2, sol, lnp_ef,img_file)
            st.pyplot(fig = fig2)

        with c22:
            c22.title('Tablas')
            st.write('VALORES MEDIOS')
            st.write(sol['df_medios_' + lnp_ef])
            st.write('VALORES MEDIOS DIFERENCIADOS')
            st.write(sol['df_dif_' + lnp_ef])
            st.write('PROLIFERACIÓN')
            st.write(sol['df_dif_perc_' + lnp_ef])
