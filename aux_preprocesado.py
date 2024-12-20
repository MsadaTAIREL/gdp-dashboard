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

def bases_de_datos(resumen_series, df0):
    # Cálculo de las matrices
    df_medios_H929 = pd.concat([(pd.DataFrame(resumen_series[k]['H929']).mean(axis = 1)) for k in resumen_series], axis = 1)
    df_medios_H929.columns =resumen_series.keys()

    df_min_H929 = pd.concat([(pd.DataFrame(resumen_series[k]['H929']).min(axis = 1)) for k in resumen_series], axis = 1)
    df_min_H929.columns =resumen_series.keys()

    df_max_H929 = pd.concat([(pd.DataFrame(resumen_series[k]['H929']).max(axis = 1)) for k in resumen_series], axis = 1)
    df_max_H929.columns =resumen_series.keys()

    df_dif_min_H929 = pd.concat([((pd.DataFrame(resumen_series[k]['H929']) - df0).min(axis = 1)) for k in resumen_series], axis = 1)
    df_dif_min_H929.columns =resumen_series.keys()

    df_dif_max_H929 = pd.concat([((pd.DataFrame(resumen_series[k]['H929']) - df0).max(axis = 1)) for k in resumen_series], axis = 1)
    df_dif_max_H929.columns =resumen_series.keys()
    df_dif_H929 = pd.DataFrame({k:df_medios_H929[k] - df0.mean(axis = 1)  for k in df_medios_H929.columns })
    df_dif_perc_H929 = pd.DataFrame({k:df_dif_H929[k] / df_dif_H929['SCR'] *100 for k in df_dif_H929.columns })
    
        # Cálculo de las matrices
    df_medios_KMS28 = pd.concat([(pd.DataFrame(resumen_series[k]['KMS28']).mean(axis = 1)) for k in resumen_series], axis = 1)
    df_medios_KMS28.columns =resumen_series.keys()

    df_min_KMS28 = pd.concat([(pd.DataFrame(resumen_series[k]['KMS28']).min(axis = 1)) for k in resumen_series], axis = 1)
    df_min_KMS28.columns =resumen_series.keys()

    df_max_KMS28 = pd.concat([(pd.DataFrame(resumen_series[k]['KMS28']).max(axis = 1)) for k in resumen_series], axis = 1)
    df_max_KMS28.columns =resumen_series.keys()

    df_dif_min_KMS28 = pd.concat([((pd.DataFrame(resumen_series[k]['KMS28']) - df0).min(axis = 1)) for k in resumen_series], axis = 1)
    df_dif_min_KMS28.columns =resumen_series.keys()

    df_dif_max_KMS28 = pd.concat([((pd.DataFrame(resumen_series[k]['KMS28']) - df0).max(axis = 1)) for k in resumen_series], axis = 1)
    df_dif_max_KMS28.columns =resumen_series.keys()

    df_dif_KMS28 = pd.DataFrame({k:df_medios_KMS28[k] - df0.mean(axis = 1)  for k in df_medios_KMS28.columns })
    df_dif_perc_KMS28 = pd.DataFrame({k:df_dif_KMS28[k] / df_dif_KMS28['SCR'] *100 for k in df_dif_KMS28.columns })
    sol = {
    'df_medios_H929': df_medios_H929,    
    'df_min_H929': df_min_H929,    
    'df_max_H929': df_max_H929,    
    'df_dif_min_H929': df_dif_min_H929,    
    'df_dif_max_H929': df_dif_max_H929,    
    'df_dif_H929': df_dif_H929,   
    'df_dif_perc_H929': df_dif_perc_H929,
    'df_medios_KMS28' : df_medios_KMS28, 
    'df_min_KMS28' : df_min_KMS28,
    'df_max_KMS28' : df_max_KMS28,
    'df_dif_min_KMS28' : df_dif_min_KMS28,
    'df_dif_max_KMS28' : df_dif_max_KMS28,
    'df_dif_KMS28' : df_dif_KMS28,
    'df_dif_perc_KMS28': df_dif_perc_KMS28
    }
    return sol