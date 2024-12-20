import pandas as pd
import matplotlib.pyplot as plt

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
    ax.set_xlabel('Time (days)', size = 15)
    
def img_1(sol, df0, lnp,img_file):
    df_medios =    sol['df_medios_'+ lnp]
    df_min =       sol['df_min_'+ lnp]
    df_max =       sol['df_max_'+ lnp]
    df_dif =       sol['df_dif_'+ lnp]
    df_dif_min =   sol['df_dif_min_'+ lnp]
    df_dif_max =   sol['df_dif_max_'+ lnp]
    fig, ax = plt.subplots(figsize = (8,2.5), ncols = 2)
    plot_bigotes(ax[0], df_medios, df_min, df_max, df0 = df0)
    ax[0].legend(['CT ('+lnp+')', 'SCT ('+lnp+')', 'RRM1 ('+lnp+')', 'Background'], fontsize = 7)
    ax[0].set_xticks(df_medios.index)
    ax[0].set_title('Mean Values', size = 15)
    plot_bigotes(ax[1], df_dif, df_dif_min, df_dif_max)
    ax[1].set_xticks(df_medios.index)
    ax[1].legend(['CT ('+lnp+')', 'SCT ('+lnp+')', 'RRM1 ('+lnp+')'], fontsize = 7)
    ax[1].set_title('Diferences Mean Values', size = 15)
    fig.savefig(img_file+"/"+'Valores_'+ lnp + '.png', bbox_inches='tight', pad_inches = 0)
    return fig

def img_2(sol, lnp,img_file, colores = {'r':'#bf775f', 'o':'#d3a65f',  'y':'#e6d26b','g':'#8bac86', 'c':'#98cacd','b':'#709acd', 'p':'#8176a7',  'gr': '#444444'}):
    df_dif = sol['df_dif_'+lnp]
    df_dif_perc = pd.DataFrame({k:df_dif[k] / df_dif['SCR'] *100 for k in df_dif.columns })
    fig, ax = plt.subplots(figsize = (8,2))
    ax.plot(df_dif_perc['CT'],   c = colores['o'],marker = '.', ms = 10)
    ax.plot(df_dif_perc['SCR'],  c = colores['r'],marker = '.', ms = 10)
    ax.plot(df_dif_perc['RRM1'], c = colores['b'],marker = '.', ms = 10)
    ax.set_title('Proliferation', size = 15)
    ax.set_xlabel('Time (days)', size = 15)
    ax.set_ylim(0,150)
    ax.legend(['CT ('+lnp+')', 'SCT ('+lnp+')', 'RRM1 ('+lnp+')'], fontsize = 7)
    ax.set_xticks(df_dif_perc.index)
    fig.savefig(img_file+"/"+'proliferacion_'+lnp + '.png', bbox_inches='tight', pad_inches = 0)