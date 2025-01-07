import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()
from aux_img import img_1, img_2
from aux_preprocesado import preprocesado, preprocesado_columnas, bases_de_datos

st.set_page_config(page_title="Análisis eficiencia", layout="wide")
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
        width: 400px;
        margin-left: -400px;
    }
     
    """,
    unsafe_allow_html=True,
)


_,c1,c2,_ = st.columns([0.3, 1,2,0.3])


with c1:
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, sep = ';')
        st.write(df)

        img_file = '/workspaces/gdp-dashboard/Img'

        c_met, c_lnp, c_dia, c_id = preprocesado_columnas(df)
        resumen_series, df0 = preprocesado(df)
        sol = bases_de_datos(resumen_series, df0)
        
        

with c2:
    if uploaded_file is not None:
        fig, ax = plt.subplots(figsize = (8,2.5), ncols = 2)
        img_1(fig, ax, sol, df0, 'H929',img_file)
        st.pyplot(fig = fig)
        fig2, ax2 = plt.subplots(figsize = (8,2.5))
        img_2(fig2, ax2, sol, 'H929',img_file)
        st.pyplot(fig = fig2)