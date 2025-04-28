import pandas as pd
import numpy as np

def preprocesado_columnas(df):
    c_met = df.columns[0]
    c_lnp = df.columns[1]
    c_dia = df.columns[2]
    c_id = df.columns[3:]
    return c_met, c_lnp, c_dia, c_id
def preprocesado(df):
    c_met, c_lnp, c_dia, c_id = preprocesado_columnas(df)

    for c in c_id:
        df[c] = [np.nan if pd.isna(el) else float(el.replace(',','.')) for el in df[c]]
    #
    # Recuperamos el Background
    df0 = df.loc[df[c_met] == 'Background']
    df0 = df0.drop_duplicates('DIA')
    df0.index = df0['DIA']
    df0 = df0[c_id]
    df1 = df.loc[df[c_met] != 'Background']
    resumen_series = {}
    for met in df1[c_met].unique():
        resumen_series[met] = {}
        df1_met = df1.loc[df1[c_met] == met]
        for lnp in df1[c_lnp]:
            resumen_series[met][lnp] = {}
            
            df1_met_lnp = df1_met.loc[df1_met[c_lnp] == lnp]
            for id in c_id:
                s = pd.Series(df1_met_lnp[id])
                s.index = df1_met_lnp[c_dia]
                s = s[~s.isna()]
                resumen_series[met][lnp][id] = s
    return resumen_series, df0

def bases_de_datos(resumen_series, df0, l_lnp):
    sol = {}
    for lnp in l_lnp:
        # Cálculo de las matrices
        df_medios = pd.concat([(pd.DataFrame(resumen_series[k][lnp]).mean(axis = 1)) for k in resumen_series], axis = 1)
        df_medios.columns =resumen_series.keys()
        #
        df_min = pd.concat([(pd.DataFrame(resumen_series[k][lnp]).min(axis = 1)) for k in resumen_series], axis = 1)
        df_min.columns =resumen_series.keys()
        #
        df_max = pd.concat([(pd.DataFrame(resumen_series[k][lnp]).max(axis = 1)) for k in resumen_series], axis = 1)
        df_max.columns =resumen_series.keys()
        #
        df_dif_min = pd.concat([((pd.DataFrame(resumen_series[k][lnp]) - df0).min(axis = 1)) for k in resumen_series], axis = 1)
        df_dif_min.columns =resumen_series.keys()
        #
        df_dif_max = pd.concat([((pd.DataFrame(resumen_series[k][lnp]) - df0).max(axis = 1)) for k in resumen_series], axis = 1)
        df_dif_max.columns =resumen_series.keys()
        df_dif = pd.DataFrame({k:df_medios[k] - df0.mean(axis = 1)  for k in df_medios.columns })
        df_dif_perc = pd.DataFrame({k:df_dif[k] / df_dif['SCR'] *100 for k in df_dif.columns })
        df_dif_perc.loc[0] = [100,100,100]
        df_dif_perc.sort_index(inplace=True)
        #
        sol['df_medios_' + lnp] = df_medios    
        sol['df_min_' + lnp] = df_min    
        sol['df_max_' + lnp] = df_max    
        sol['df_dif_min_' + lnp] = df_dif_min    
        sol['df_dif_max_' + lnp] = df_dif_max    
        sol['df_dif_' + lnp] = df_dif   
        sol['df_dif_perc_' + lnp] = df_dif_perc
    return sol
def procesar_datos_v(df, col_v, col_id, col_dia):
    series = {}
    for id in df[col_id].unique():
        df_id = df.loc[df[col_id] == id]
        s_v = pd.Series(list(df_id[col_v]), index = df_id[col_dia])
        s_v.sort_index(inplace= True)
        series[id] = s_v
    df_v = pd.DataFrame(series).transpose()
    for id in df[col_id].unique():
        s_v = df_v.loc[id].copy()
        if any(s_v.isna()):
            na_i = np.arange(len(s_v))[s_v.isna()]
            for i in na_i:
                if i ==0:# preguntar
                    s_v[s_v.index[0]] = 0
                elif i ==len(s_v)-1:
                    s_v[s_v.index[i]] = s_v[s_v.index[i-1]]
                else:
                    d0, d1, d2 = s_v.index[i-1:i+2]
                    s_v[d1] = s_v[d0] + (s_v[d2] - s_v[d0]) / (d2-d0) * (d1 - d0)
            series[id] = s_v
    df_v = pd.DataFrame(series).transpose()
    return df_v
def preprocesar_df_est(df_v, met):
    df_v = df_v.copy()
    df_aux = df_v.loc[[id.split('_')[0] == met for id in df_v.index]]
    return pd.DataFrame({met + '_min':df_aux.min(),met + '_max': df_aux.max(), met + '_mean':df_aux.mean()})
def calcular_prol_vivo(df_vol, control_vv, tratamiento_vv):
    df_control = preprocesar_df_est(df_vol, control_vv)
    df_tratamiento = preprocesar_df_est(df_vol, tratamiento_vv)
    prol = df_tratamiento[tratamiento_vv + '_mean'] / df_control[control_vv + '_mean'] * 100 
    prol[df_control[control_vv + '_mean'] == 0] = 100
    return prol