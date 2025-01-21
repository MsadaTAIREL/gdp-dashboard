import pandas as pd
import matplotlib.pyplot as plt
from aux_preprocesado import preprocesar_df_est

def plot_bigotes(ax, df_mean, df_min, df_max,colores = {'r':'#bf775f', 'o':'#d3a65f',  'y':'#e6d26b','g':'#8bac86', 'c':'#98cacd','b':'#709acd', 'p':'#8176a7',  'gr': '#444444'}, df0 = None):
    
    
    ax.plot(df_mean['CT'],       c = colores['o'],    marker = '.', ms = 10)
    ax.plot(df_mean['SCR'],      c = colores['r'],    marker = '.', ms = 10)
    ax.plot(df_mean['RRM1'],     c = colores['b'],    marker = '.', ms = 10)
    if type(df0)!= type(None):
        ax.plot(df0.mean(axis = 1), marker = '.', ms = 10, c = colores['gr'], linestyle = '-.')
        for d in df_mean.index:ax.plot([d]*2, [df0.min(axis=1)[d],df0.max(axis=1)[d]], c = colores['gr'],    marker = '_', ms = 10)
    for d in df_mean.index:ax.plot([d]*2, [df_min.loc[d, 'CT'], df_max.loc[d, 'CT']], c = colores['o'],    marker = '_', ms = 10)
    for d in df_mean.index:ax.plot([d]*2, [df_min.loc[d, 'SCR'], df_max.loc[d, 'SCR']], c = colores['r'],    marker = '_', ms = 10)
    for d in df_mean.index:ax.plot([d]*2, [df_min.loc[d, 'RRM1'], df_max.loc[d, 'RRM1']], c = colores['b'],    marker = '_', ms = 10)
    ax.set_xlabel('Time (days)', size = 12)
    
def img_1(fig, ax,sol, df0, lnp,img_file):
    df_medios =    sol['df_medios_'+ lnp]
    df_min =       sol['df_min_'+ lnp]
    df_max =       sol['df_max_'+ lnp]
    df_dif =       sol['df_dif_'+ lnp]
    df_dif_min =   sol['df_dif_min_'+ lnp]
    df_dif_max =   sol['df_dif_max_'+ lnp]
    plot_bigotes(ax[0], df_medios, df_min, df_max, df0 = df0)
    ax[0].legend(['CT ('+lnp+')', 'SCT ('+lnp+')', 'RRM1 ('+lnp+')', 'Background'], fontsize = 8)
    ax[0].set_xticks(df_medios.index)
    ax[0].set_title('Mean Values', size = 12)
    plot_bigotes(ax[1], df_dif, df_dif_min, df_dif_max)
    ax[1].set_xticks(df_medios.index)
    ax[1].legend(['CT ('+lnp+')', 'SCT ('+lnp+')', 'RRM1 ('+lnp+')'], fontsize = 8)
    ax[1].set_title('Diferences Mean Values', size = 12)
    fig.savefig(img_file+'/Valores_'+ lnp + '.png', bbox_inches='tight', pad_inches = 0)

def img_2(fig, ax,sol, lnp,img_file, colores = {'r':'#bf775f', 'o':'#d3a65f',  'y':'#e6d26b','g':'#8bac86', 'c':'#98cacd','b':'#709acd', 'p':'#8176a7',  'gr': '#444444'}):
    df_dif_perc = sol['df_dif_perc_'+lnp]
    ax.plot(df_dif_perc['CT'],   c = colores['o'],marker = '.', ms = 10)
    ax.plot(df_dif_perc['SCR'],  c = colores['r'],marker = '.', ms = 10)
    ax.plot(df_dif_perc['RRM1'], c = colores['b'],marker = '.', ms = 10)
    ax.set_title('Proliferation', size = 12)
    ax.set_xlabel('Time (days)', size = 12)
    ax.set_ylim(0,150)
    ax.legend(['CT ('+lnp+')', 'SCT ('+lnp+')', 'RRM1 ('+lnp+')'], fontsize = 8)
    ax.set_xticks(df_dif_perc.index)
    fig.savefig(img_file+'/proliferacion_'+lnp + '.png', bbox_inches='tight', pad_inches = 0)

def plot_line_bigotes(ax, s_mean, s_min, s_max, c = '#709acd'):
    v = ax.plot(s_mean, c = c, marker = '.', ms = 10)
    for d in s_mean.index:ax.plot([d]*2, [s_min[d], s_max[d]], c =c, alpha = 0.75,marker = '_', ms = 10)
    return v
def img_3(df_v1, df_v2, df_v3, bigotes = False, colores = {'r':'#bf775f', 'o':'#d3a65f',  'y':'#e6d26b','g':'#8bac86', 'c':'#98cacd','b':'#709acd', 'p':'#8176a7',  'gr': '#444444'}):
    fig, ax = plt.subplots(figsize = (12,3), ncols = 3, sharey=True)

    for i in range(3):
        graf = []
        df_v = [df_v1, df_v2, df_v3][i]
        for j in range(2):
            met = ['Control', 'Tratamiento'][j]
            df_aux = preprocesar_df_est(df_v, met)
            if bigotes:
                v = plot_line_bigotes(ax[i], df_aux[met + '_mean'],df_aux[met + '_min'],df_aux[met + '_max'], c = colores[['o','b'][j]])
            else:
                ax[i].fill_between(df_aux.index,df_aux[met + '_min'],df_aux[met + '_max'], alpha = 0.3, color = colores[['o','b'][j]])
                v = ax[i].plot(df_aux[met + '_mean'], c = colores[['o','b'][j]], marker = '.', ms = 10)
            graf.append(v[0])
        ax[i].set_xlabel('Time (days)')
    ax[0].set_ylabel('Width')
    ax[1].set_ylabel('Length')
    ax[2].set_ylabel('Deep')
    ax[0].legend(graf,['Control','Tratamiento'])
    return fig, ax
def img_4(df_vol, bigotes= True, colores = {'r':'#bf775f', 'o':'#d3a65f',  'y':'#e6d26b','g':'#8bac86', 'c':'#98cacd','b':'#709acd', 'p':'#8176a7',  'gr': '#444444'}):
    fig, ax = plt.subplots(figsize = (12,3))
    graf = []
    for j in range(2):
        met = ['Control', 'Tratamiento'][j]
        df_aux = preprocesar_df_est(df_vol, met)
        if bigotes:
            v = plot_line_bigotes(ax, df_aux[met + '_mean'],df_aux[met + '_min'],df_aux[met + '_max'], c = colores[['o','b'][j]])
        else:
            ax.fill_between(df_aux.index,df_aux[met + '_min'],df_aux[met + '_max'], alpha = 0.3, color = colores[['o','b'][j]])
            v = ax.plot(df_aux[met + '_mean'], c = colores[['o','b'][j]], marker = '.', ms = 10)
        graf.append(v[0])
    ax.legend(graf,['Control','Tratamiento'])
    ax.set_ylabel('Volume')
    return fig, ax
def img_5(df_vol, colores = {'r':'#bf775f', 'o':'#d3a65f',  'y':'#e6d26b','g':'#8bac86', 'c':'#98cacd','b':'#709acd', 'p':'#8176a7',  'gr': '#444444'}):
    df_control = preprocesar_df_est(df_vol, 'Control')
    df_tratamiento = preprocesar_df_est(df_vol, 'Tratamiento')
    prol = df_tratamiento['Tratamiento_mean'] / df_control['Control_mean'] * 100 
    prol[df_control['Control_mean'] == 0] = 100
    fig, ax = plt.subplots(figsize = (12,3))
    ax.set_ylabel('Proliferation')
    ax.set_xlabel('Time (days)')
    ax.plot(prol * 0 + 100, c = colores['o'], marker = '.', ms = 10)
    ax.plot(prol, c = colores['b'], marker = '.', ms = 10)
    return fig, ax