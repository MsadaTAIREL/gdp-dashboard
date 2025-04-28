import pandas as pd
import matplotlib.pyplot as plt
from aux_preprocesado import preprocesar_df_est,calcular_prol_vivo

    
def img_1(fig, ax,sol, df0, lnp,img_file,bigotes = True,colores = {'r':'#bf775f', 'o':'#d3a65f',  'y':'#e6d26b','g':'#8bac86', 'c':'#98cacd','b':'#709acd', 'p':'#8176a7',  'gr': '#444444'}):
    df_medios =    sol['df_medios_'+ lnp]
    df_min =       sol['df_min_'+ lnp]
    df_max =       sol['df_max_'+ lnp]
    df_dif =       sol['df_dif_'+ lnp]
    df_dif_min =   sol['df_dif_min_'+ lnp]
    df_dif_max =   sol['df_dif_max_'+ lnp]
    #
    aux_leg = []
    if bigotes:
        for met in ['CT','SCR','RRM1']:
            aux_leg.append( plot_line_bigotes(ax[0], df_medios[met],   df_min[met], df_max[met], c = colores[{'CT': 'o', 'SCR': 'r', 'RRM1': 'b'}[met]])[0])
    else:
        for met in ['CT','SCR','RRM1']:
            c =  colores[{'CT': 'o', 'SCR': 'r', 'RRM1': 'b'}[met]]
            ax[0].fill_between(df_min.index, df_min[met],df_max[met], alpha = 0.3, color = c)
            aux_leg.append(ax[0].plot(df_medios[met], c = c, marker = '.', ms = 10)[0])
    aux_leg.append(ax[0].plot(df0.mean(axis = 1), marker = '.', ms = 10, c = colores['gr'], linestyle = '-.')[0])
    #
    ax[0].legend(aux_leg,['CT ('+lnp+')', 'SCR ('+lnp+')', 'RRM1 ('+lnp+')', 'Background'], fontsize = 8)
    ax[0].set_xticks(df_medios.index)
    ax[0].set_title('Valores medios', size = 12)
    ax[0].set_xlabel('Tiempo (días)', size = 12)
    #
    #
    aux_leg = []
    if bigotes:
        for met in ['CT','SCR','RRM1']:
            aux_leg.append( plot_line_bigotes(ax[1], df_dif[met],   df_dif_min[met], df_dif_max[met], c = colores[{'CT': 'o', 'SCR': 'r', 'RRM1': 'b'}[met]])[0])
    else:
        for met in ['CT','SCR','RRM1']:
            c =  colores[{'CT': 'o', 'SCR': 'r', 'RRM1': 'b'}[met]]
            ax[1].fill_between(df_dif.index,df_dif_min[met],df_dif_max[met], alpha = 0.3, color = c)
            aux_leg.append(ax[1].plot(df_dif[met], c = c, marker = '.', ms = 10)[0])

    ax[1].set_xticks(df_medios.index)
    ax[1].legend(aux_leg,['CT ('+lnp+')', 'SCT ('+lnp+')', 'RRM1 ('+lnp+')'], fontsize = 8)
    ax[1].set_title('Valores medios diferenciados', size = 12)
    ax[1].set_xlabel('Tiempo (días)', size = 12)
    fig.savefig(img_file+'/Valores_'+ lnp + '.png', bbox_inches='tight', pad_inches = 0)

def img_2(fig, ax,sol, lnp,img_file, colores = {'r':'#bf775f', 'o':'#d3a65f',  'y':'#e6d26b','g':'#8bac86', 'c':'#98cacd','b':'#709acd', 'p':'#8176a7',  'gr': '#444444'}):
    df_dif_perc = sol['df_dif_perc_'+lnp]
    ax.plot(df_dif_perc['CT'],   c = colores['o'],marker = '.', ms = 10)
    ax.plot(df_dif_perc['SCR'],  c = colores['r'],marker = '.', ms = 10)
    ax.plot(df_dif_perc['RRM1'], c = colores['b'],marker = '.', ms = 10)
    ax.set_title('Proliferación', size = 12)
    ax.set_xlabel('Tiempo (días)', size = 12)
    ax.set_ylim(0,150)
    ax.legend(['CT ('+lnp+')', 'SCT ('+lnp+')', 'RRM1 ('+lnp+')'], fontsize = 8)
    ax.set_xticks(df_dif_perc.index)
    fig.savefig(img_file+'/proliferacion_'+lnp + '.png', bbox_inches='tight', pad_inches = 0)

def plot_line_bigotes(ax, s_mean, s_min, s_max, c = '#709acd'):
    v = ax.plot(s_mean, c = c, marker = '.', ms = 10)
    for d in s_mean.index:ax.plot([d]*2, [s_min[d], s_max[d]], c =c, alpha = 0.75,marker = '_', ms = 10)
    return v
def img_3(fig,ax, df_v1, df_v2, df_v3,control_vv, tratamiento_vv, bigotes = False, img_file = None,colores = {'r':'#bf775f', 'o':'#d3a65f',  'y':'#e6d26b','g':'#8bac86', 'c':'#98cacd','b':'#709acd', 'p':'#8176a7',  'gr': '#444444'}):

    for i in range(3):
        graf = []
        df_v = [df_v1, df_v2, df_v3][i]
        for j in range(2):
            met = [control_vv, tratamiento_vv][j]
            df_aux = preprocesar_df_est(df_v, met)
            if bigotes:
                v = plot_line_bigotes(ax[i], df_aux[met + '_mean'],df_aux[met + '_min'],df_aux[met + '_max'], c = colores[['o','b'][j]])
            else:
                ax[i].fill_between(df_aux.index,df_aux[met + '_min'],df_aux[met + '_max'], alpha = 0.3, color = colores[['o','b'][j]])
                v = ax[i].plot(df_aux[met + '_mean'], c = colores[['o','b'][j]], marker = '.', ms = 10)
            graf.append(v[0])
        ax[i].set_xlabel('Tiempo (días)')
    ax[0].set_title('V1' , size = 12)
    ax[1].set_title('V2', size = 12)
    ax[2].set_title('V3'  , size = 12)
    ax[0].legend(graf,[control_vv, tratamiento_vv])
    if type(img_file) == str:
        fig.savefig(img_file+'/img3' + '.png', bbox_inches='tight', pad_inches = 0)
def img_4(fig, ax,df_vol, control_vv, tratamiento_vv,bigotes= True,img_file = None, colores = {'r':'#bf775f', 'o':'#d3a65f',  'y':'#e6d26b','g':'#8bac86', 'c':'#98cacd','b':'#709acd', 'p':'#8176a7',  'gr': '#444444'}):
    graf = []
    for j in range(2):
        met = [control_vv, tratamiento_vv][j]
        df_aux = preprocesar_df_est(df_vol, met)
        if bigotes:
            v = plot_line_bigotes(ax, df_aux[met + '_mean'],df_aux[met + '_min'],df_aux[met + '_max'], c = colores[['o','b'][j]])
        else:
            ax.fill_between(df_aux.index,df_aux[met + '_min'],df_aux[met + '_max'], alpha = 0.3, color = colores[['o','b'][j]])
            v = ax.plot(df_aux[met + '_mean'], c = colores[['o','b'][j]], marker = '.', ms = 10)
        graf.append(v[0])
    ax.set_xlabel('Tiempo (días)')
    ax.legend(graf,[control_vv, tratamiento_vv])
    ax.set_ylabel('Volumen')
    if type(img_file) == str:
        fig.savefig(img_file+'/img4' + '.png', bbox_inches='tight', pad_inches = 0)
def img_5(fig, ax,df_vol,control_vv, tratamiento_vv,img_file = None, colores = {'r':'#bf775f', 'o':'#d3a65f',  'y':'#e6d26b','g':'#8bac86', 'c':'#98cacd','b':'#709acd', 'p':'#8176a7',  'gr': '#444444'}):
    prol = calcular_prol_vivo(df_vol, control_vv, tratamiento_vv)
    ax.set_ylabel('Proliferación')
    ax.set_xlabel('Tiempo (días)')
    ax.plot(prol * 0 + 100, c = colores['o'], marker = '.', ms = 10)
    ax.plot(prol, c = colores['b'], marker = '.', ms = 10)
    ax.legend([control_vv, tratamiento_vv])
    if type(img_file) == str:
        fig.savefig(img_file+'/img5' + '.png', bbox_inches='tight', pad_inches = 0)
