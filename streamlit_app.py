import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
#from aux_img import img_1, img_2
from aux_preprocesado import preprocesado, preprocesado_columnas, bases_de_datos
st.title("Análisis eficiencia")
c1,c2 = st.columns(2)

with c1:
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, sep = ';')
        st.write(df)

        img_file = '/workspaces/gdp-dashboard/Img'

        c_met, c_lnp, c_dia, c_id = preprocesado_columnas(df)
        resumen_series, df0 = preprocesado(df)
        sol = bases_de_datos(resumen_series, df0)

