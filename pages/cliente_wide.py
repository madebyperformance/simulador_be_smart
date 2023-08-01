import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import datetime as DT
import math
import time as tm
from func.redirect import nav_page
from st_aggrid import JsCode, AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
from st_aggrid.shared import GridUpdateMode, AgGridTheme
from database import base_df, besmart_base, PositivadorBitrix, besmart_base_2
import locale
import requests


locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
custom_css = {".ag-theme-alpine": {
            "--ag-background-color": "#fff !important",
            "--ag-foreground-color": "#181d1f !important",
            "--ag-subheader-background-color": "#fff !important",
            "--ag-alpine-active-color": "#EBFF70 !important",
            "--ag-range-selection-border-color": "#EBFF70 !important",
            "font-family": ' "Barlow" !important'}}

#try:
v3 = st.session_state.df_cliente.client_id[0]

st.set_page_config(
    page_icon="invest_smart_logo.png",
    page_title="Simulador - Ativos 0.55",
    initial_sidebar_state="collapsed",
    layout="wide",
)

df = PositivadorBitrix().get_produto_cliente_id(int(v3))
#df = PositivadorBitrix().get_produto_v2()
df = df.rename(columns={
    st.secrets.VAR_ID_CLIENTE:'client_id',
    st.secrets.VAR_EMPRESA:'empresa',
    st.secrets.VAR_CATEGORIA:'categoria',
    st.secrets.VAR_ATIVO:'ativo',
    st.secrets.VAR_PL_APLICADO:'pl_aplicado',
    st.secrets.VAR_RETORNO:'retorno',
    st.secrets.VAR_REPASSE:'repasse',
    st.secrets.VAR_ROA_HEAD:'roa_head',
    st.secrets.VAR_ROA_REC:'roa_rec',
    st.secrets.VAR_DATA_ATIVO:'data_ativo',
    st.secrets.VAR_DATA_VENC:'data_venc',
    st.secrets.id:'ativo_id',
    })

#st.dataframe(df)
name_v1 = st.session_state.df_cliente["Nome do Cliente"][0]
dt_cads = st.session_state.df_cliente["Data de Cadastro"][0]

dark = df.copy()

dark = dark.rename(
    columns={
        "categoria": "Categoria",
        "ativo": "Ativo",
        "pl_aplicado": "PL Aplicado",
        "data_venc": "Data de Vencimento",
        "data_ativo": "Data de Início",
        "empresa": "Empresa",
    }
)
dark['PL Aplicado']= dark['PL Aplicado'].astype(float)
dark['PL Aplicado']= dark['PL Aplicado'].astype(int)
dark['client_id']= dark['client_id'].astype(int)
dark['retorno']= dark['retorno'].astype(float)
dark['repasse']= dark['repasse'].astype(float)
dark['roa_head']= dark['roa_head'].astype(float)
dark['roa_rec']= dark['roa_rec'].astype(float)
dark['ativo_id']= dark['ativo_id'].astype(int)

df_ativo = dark.copy()




#st.dataframe(dark)

col1, mid, direita2 = st.columns([12,8,4])
with col1:
    st.write(
        fr'<p style="font-size:30px;">Nome do Cliente: {name_v1}</p>',
        unsafe_allow_html=True,
    )

    st.write(
        fr'<p style="font-size:30px;">Portifólios</p>',
        unsafe_allow_html=True,
    )
    if st.button("Voltar a visão Geral do Assessor"):
        nav_page("wide_project")
with direita2:
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    esquerda3, direita3  = st.columns([4, 5])
    with direita3:
        if st.button('Logout',key='logout3'):
            st.session_state["logout"] =None
            if st.session_state["logout"]==None:
                nav_page('')


st.markdown(
    """
    <hr style="height:1px;border:none;color:#9966ff;background-color:#9966ff;" /> 
    """,
    unsafe_allow_html=True,
)


font_css = """
<style>
button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
font-size: 24px;
}
</style>
"""
st.write(font_css, unsafe_allow_html=True)








    
nulo12, nulo22, col22 = st.columns([12, 8, 5])
with col22:
    st.text("")
    st.text("")
    st.image("BeSmart_Logos_AF_horizontal__branco.png", width=270)
    
vacuo141, retorno2, ano1_avg2, ano2_avg2 = st.columns([ 1.5,5, 5, 3])

face_v2 = pd.read_excel("base_besmart_v3.xlsx")
face_v2["Categoria"] = face_v2["Categoria"].apply(lambda x: x.replace("_", " "))
face_v2["Produto"] = face_v2["Produto"].apply(lambda x: x.replace("_", " "))
face_v2["porcem_repasse"] = face_v2["porcem_repasse"] * 100.0



smart = pd.DataFrame(columns=["Mês", "Resultado assessor",'Faturamento','Resultado Bruto'])
for i in dark["ativo_id"].unique():
                df_v2 = dark[dark["ativo_id"] == i]
                df_v2 = df_v2.reset_index().drop("index", 1)
                if df_v2.Empresa.iloc[0] == "INVESTSMART":
                    grasph_df = base_df(
                        df_v2["Data de Vencimento"].iloc[0],
                        df_v2["Data de Início"].iloc[0],
                        float(
                            df_v2["PL Aplicado"]
                            .iloc[0][3:]
                            .replace(".", "")
                            .replace(",", ".")
                        ),
                        df_v2.retorno.iloc[0],
                        df_v2.roa_head.iloc[0],
                        df_v2.roa_rec.iloc[0],
                        st.session_state.reps_investsmart,
                        moeda_real=False,
                    )
                    grasph_df["ativo_id"] = i
                else:
                    if df_v2.Empresa.iloc[0] == "Seguros":
                        repasse1 = st.session_state.reps_seguro
                    elif df_v2.Empresa.iloc[0] == "Câmbio":
                        repasse1 = st.session_state.reps_cambio
                    elif df_v2.Empresa.iloc[0] == "Crédito":
                        repasse1 = st.session_state.reps_credito
                    else:
                        repasse1 = st.session_state.reps_imovel

                    grasph_df = besmart_base(
                        df_v2["Data de Vencimento"].iloc[0],
                        df_v2["Data de Início"].iloc[0],
                        face_v2,
                        df_v2.Empresa.iloc[0],
                        df_v2.Categoria.iloc[0],
                        df_v2.Ativo.iloc[0],
                        float(
                            df_v2["PL Aplicado"]
                            .replace(".", "")
                            .replace(",", ".")
                        ),
                        repasse1,
                    )
                    grasph_df["ativo_id"] = i
                # st.dataframe(grasph_df)
                smart = smart.append(grasph_df)
            #st.dataframe(smart)
smart["Mês"] = smart["Mês"].apply(
                lambda x: DT.datetime.strptime(x, "%b-%y")
            )
smart["Mês"] = smart["Mês"].apply(
                lambda x: DT.datetime.strftime(x, "%m-%y")
            )
mapas = dict(dark[["ativo_id","Ativo"]].values)
smart["Produtos"] = smart.ativo_id.map(mapas)

try:
    smart['Total Bruto'] = smart['Faturamento'].fillna(0) + smart['Resultado Bruto'].fillna(0)
except:
    try:
        smart['Total Bruto'] = smart['Faturamento'].fillna(0)
    except:
        smart['Total Bruto'] = smart['Resultado Bruto'].fillna(0)
#st.dataframe(smart)

final = (
                smart[["Mês", "Resultado assessor","Produtos",'Total Bruto']]
                .groupby(["Mês","Produtos"]).sum()
                .reset_index()
            )

final["Mês"] = final["Mês"].apply(
    lambda x: DT.datetime.strptime(x, "%m-%y")
)
final["ano"] = final["Mês"].astype("datetime64").dt.year
final["mes"] = final["Mês"].astype("datetime64").dt.month
final["Mês"] = final["Mês"].apply(
    lambda x: DT.datetime.strftime(x, "%b-%y")
)
final = final.sort_values(["ano", "mes"]).reset_index(drop=True)
final['Resultado assessor'] = final['Resultado assessor'].astype('float64')

final['Resultado assessor'] = final['Resultado assessor'].fillna(0)
#st.dataframe(final)
final["data"] = final["Mês"].apply(lambda x: DT.datetime.strptime(x,"%b-%y"))
final["data"] = final["data"].apply(lambda x: DT.datetime.strftime(x, "%Y/%m"))



try:
    result_month = final["Resultado assessor"][(final["mes"] == DT.datetime.now().month)& (final["ano"] == DT.datetime.now().year)].sum() 
    avrg_year1 = (final["Resultado assessor"][
        final["ano"] == DT.datetime.now().year
    ].sum())
    avrg_year2 = (final["Resultado assessor"][
        final["ano"] == DT.datetime.now().year + 1
    ].sum())
except:
    result_month = 0
    avrg_year1 = 0
    avrg_year2 = 0


try:
    final_besm = final[final["Produtos"].isin(face_v2["Produto"])]
    
    result_month2 = final_besm["Resultado assessor"][(final_besm["mes"] == DT.datetime.now().month)& (final_besm["ano"] == DT.datetime.now().year)].sum() 
    
    avrg_year12 = (final_besm["Resultado assessor"][
        final_besm["ano"] == DT.datetime.now().year
    ].sum())
    avrg_year22 = (final_besm["Resultado assessor"][
        final_besm["ano"] == DT.datetime.now().year + 1
    ].sum())
except:
    result_month2 = 0
    avrg_year12 = 0
    avrg_year22 = 0











try:
    retorno2.metric(
        "Comissão Esperada para esse mês",
        "R$ "
        + locale.currency(
            result_month,
            grouping=True,
            symbol=None,
        )[:-3],
    )
except:
    retorno2.metric(
        "Comissão Esperada para esse mês",
        "R$ "
        + locale.currency(
            0,
            grouping=True,
            symbol=None,
        )[:-3],
    )

ano1_avg2.metric(
    f"Comissão Esperada {DT.datetime.now().year}",
    "R$ "
    + locale.currency(
        avrg_year12,
        grouping=True,
        symbol=None,
    )[:-3],
)

if np.isnan(avrg_year2):
    ano2_avg2.metric(
        f"Comissão Esperada {DT.datetime.now().year+1}",
        "R$ "
        + locale.currency(
            0,
            grouping=True,
            symbol=None,
        )[:-3],
    )
else:
    ano2_avg2.metric(
        f"Comissão Esperada {DT.datetime.now().year+1}",
        "R$ "
        + locale.currency(
            avrg_year22,
            grouping=True,
            symbol=None,
        )[:-3],
    )




















st.write("")
st.write("")
vacuo,  botao22, botao32, botao42, vacuo = st.columns([7,5, 5,5,7])

        
vazio1, cliente, vazio2 = st.columns([1, 9, 1])
with cliente:
    dark3 = dark[dark["Empresa"]!="INVESTSMART"]


    dark3 = dark3.rename(columns = {"Ativo":"Produto","PL Aplicado":"Valor do Produto"})
    

    gridOptions = GridOptionsBuilder.from_dataframe(
        dark3[
            [
                # "client_id",
                "Empresa",
                "Categoria",
                "Produto",
                "Valor do Produto",
                "Data de Início",
                "Data de Vencimento",
                # "shelf_id",
            ]
        ]
    )

    gridOptions.configure_selection(
        selection_mode="single", use_checkbox=True, pre_selected_rows=[0]
    )

    gb = gridOptions.build()

    mycntnr = st.container()
    with mycntnr:
        htmlstr = f'''<p style='background-color: #9966ff;  font-family: "Knockout"; color: #FFF; font-size: 20px; border-radius: 7px; padding-left: 8px; text-align: center'>Tabela de Produtos</style></p>'''
        st.markdown(htmlstr, unsafe_allow_html=True)

        dta2 = AgGrid(
            dark3,
            gridOptions=gb,
            #height=290,
            # width=5000,
            allow_unsafe_jscode=True,
            theme=AgGridTheme.ALPINE,
            fit_columns_on_grid_load =True,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
            reload_data=True,
            key="besmart_grid",
            custom_css=custom_css
        )
    st.markdown(
        """
        <hr style="height:1px;border:none;color:#9966ff;background-color:#9966ff;" /> 
        """,
        unsafe_allow_html=True,
    )
  






st.session_state["df_ativo2"] = pd.DataFrame(dta2["selected_rows"])

#st.dataframe(st.session_state["df_ativo2"])

space15,choice2,space16= st.columns([6,5,5])
container3 = st.container() 
chart4= st.container()
with botao22:
    if st.button("Incluir Produto BeSmart",key="asdf"):
        st.session_state["df_ativo2"]
        nav_page("besmart_novo_ativo")
with botao32:
    if st.button("Visualizar Produto BeSmart"):
        if st.session_state["df_ativo2"].empty:
            st.error("Não foi selecionado um ativo")
        else:
            #st.session_state["df_ativo2"] = pd.DataFrame()
            st.session_state["df_ativo2"] = pd.DataFrame(dta2["selected_rows"])
            #st.dataframe(st.session_state.df_ativo2)
            nav_page("besmart_edit_ativo")
if "button442" not in st.session_state:
        st.session_state["button442"] = False
with botao42:
    if st.button("Deletar o Produto Selecionado",key=2):
        st.session_state["button442"] = not st.session_state["button442"]
    if st.session_state["button442"]:
        disco = st.write("Tem Certeza ?")
        sim, nao = st.columns(2)
        with sim:
            if st.button("Sim",key=22):
                if st.session_state["df_ativo2"].empty:
                    st.error("Não foi selecionado um Cliente")
                else:
                    vers = int(st.session_state.df_ativo2.ativo_id[0])
                    url = st.secrets.url_delete+'id'+f"={vers}"
                    payload = {}
                    headers = {
                    'Cookie': 'BITRIX_SM_SALE_UID=0'
                    }
                    response = requests.request("POST", url, headers=headers, data=payload)
                    # cursor.execute("DELETE FROM variaveis WHERE ativo_id = ?", (vers,))
                    # con.commit()
                    st.success("O ativo foi deletado com sucesso")
                    tm.sleep(1)
                    st._rerun()
        with nao:
            if st.button("Não",key=23):
                st.session_state["button442"] = False
        




invest_prod = pd.read_excel("bd_base_v3.xlsx")






with choice2:
    coluna = st.radio("Qual tipo de Gráfico é desejado ?",["Comissão Líquida - Assessor","Resultado Bruto"],horizontal=True,key='tres_O')
    if coluna == "Comissão Líquida - Assessor":
        subst = "Resultado assessor"
    else:
        subst = "Total Bruto"

if (
            st.session_state["df_cliente"]["Qnt. Ativos InvestSmart"].iloc[0]
            + st.session_state["df_cliente"]["Qnt. Produtos BeSmart"].iloc[0]
            == 0
        ):

            st.text("")
            st.error("Esse Cliente não tem Portifólio")
elif st.session_state["df_cliente"]["Qnt. Produtos BeSmart"].sum() == 0:
            st.text("")
            st.error("Esse Cliente não tem Portifólio Besmart")
else:
            smart = pd.DataFrame(columns=["Mês", "Resultado assessor",'Faturamento','Resultado Bruto'])
            for i in dark["ativo_id"].unique():
                df_v2 = dark[dark["ativo_id"] == i]
                df_v2 = df_v2.reset_index().drop("index", 1)
                

                #st.dataframe(df_v2)
                if df_v2.Empresa.iloc[0] == "INVESTSMART":
                    grasph_df = base_df(
                        df_v2["Data de Vencimento"].iloc[0],
                        df_v2["Data de Início"].iloc[0],
                        float(
                            df_v2["PL Aplicado"]

                            .replace(".", "")
                            .replace(",", ".")
                        ),
                        df_v2.retorno.iloc[0],
                        df_v2.roa_head.iloc[0],
                        df_v2.roa_rec.iloc[0],
                        st.session_state.reps_investsmart,
                        moeda_real=False,
                    )
                    grasph_df["ativo_id"] = i
                else:
                    if df_v2.Empresa.iloc[0] == "Seguros":
                        repasse1 = st.session_state.reps_seguro
                    elif df_v2.Empresa.iloc[0] == "Câmbio":
                        repasse1 = st.session_state.reps_cambio
                    elif df_v2.Empresa.iloc[0] == "Crédito":
                        repasse1 = st.session_state.reps_credito
                    else:
                        repasse1 = st.session_state.reps_imovel
                    grasph_df = besmart_base(
                        df_v2["Data de Vencimento"].iloc[0],
                        df_v2["Data de Início"].iloc[0],
                        face_v2,
                        df_v2.Empresa.iloc[0],
                        df_v2.Categoria.iloc[0],
                        df_v2.Ativo.iloc[0],
                        float(
                            df_v2["PL Aplicado"]
                            .replace(".", "")
                            .replace(",", ".")
                        ),
                        repasse1,
                    )
                    grasph_df["ativo_id"] = i
                # st.dataframe(grasph_df)
                smart = smart.append(grasph_df)
            #st.dataframe(smart)
            smart = smart[smart['Custo do Produto'].notna()]
            smart["Mês"] = smart["Mês"].apply(
                lambda x: DT.datetime.strptime(x, "%b-%y")
            )
            smart["Mês"] = smart["Mês"].apply(
                lambda x: DT.datetime.strftime(x, "%m-%y")
            )
            mapas = dict(dark[["ativo_id","Ativo"]].values)
            smart["Produtos"] = smart.ativo_id.map(mapas)
            smart['Total Bruto'] = smart['Faturamento'].fillna(0) + smart['Resultado Bruto'].fillna(0)
            #st.dataframe(smart)
            
            
            final2 = (
                smart[["Mês", "Resultado assessor","Produtos",'Total Bruto']]
                .groupby(["Mês","Produtos"]).sum()
                .reset_index()
            )
            
            #st.dataframe(final)
            
            final2["Mês"] = final2["Mês"].apply(
                lambda x: DT.datetime.strptime(x, "%m-%y")
            )
            final2["ano"] = final2["Mês"].astype("datetime64").dt.year
            final2["mes"] = final2["Mês"].astype("datetime64").dt.month
            final2["Mês"] = final2["Mês"].apply(
                lambda x: DT.datetime.strftime(x, "%b-%y")
            )
            final2 = final2.sort_values(["ano", "mes"]).reset_index(drop=True)
            #st.dataframe(final)
            final2["data"] = final2["Mês"].apply(lambda x: DT.datetime.strptime(x,"%b-%y"))
            final2["data"] = final2["data"].apply(lambda x: DT.datetime.strftime(x, "%Y/%m"))
            #st.dataframe(super_smart["data"].unique())
            distancia = list(final2["data"].unique())
            distancia_df = pd.DataFrame(distancia)
            distancia_df["ano"] = distancia_df[0].astype("datetime64").dt.year
            with container3:
                #coluna = st.radio("Escolha o Tipo de Grafico a ser observado",["Resultado assessor"])
                try:
                    i_n_v = distancia_df[distancia_df["ano"] == DT.datetime.now().year + 2].reset_index().iloc[-1]["index"]
                    inc1, end1 = st.select_slider("Período de tempo do Grafico",options = distancia,value=(distancia[0],distancia[i_n_v]),key="besmart")
                except:
                    inc1, end1 = st.select_slider("Período de tempo do Grafico",options = distancia,value=(distancia[0],distancia[-1]),key="besmart_v42")
            try:
                fig = px.bar(
                    final2[(final2["data"]>= inc1) & (final2["data"]<= end1)],
                    x="Mês",
                    y=subst,
                    color="Produtos",
                    #width=1700,
                    height=600,
                    text_auto='.2f',
                    title=f"Comissão Be.Smart Mensal",
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    labels = {subst:subst + "(R$)"}
                )
                fig.update_layout(
                    #showlegend=False,
                    legend_title= None,
                    uniformtext_minsize=8,
                    uniformtext_mode="hide",
                    legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    #xanchor="right",
                    #x=1
                    )
                    )
                fig.update_traces(textfont_size=12,textposition='inside')
                temp=final2[(final2["data"]>= inc1) & (final2["data"]<= end1)]
                temp=temp[['Mês',subst]].groupby('Mês').sum().reset_index()
                fig.add_trace(go.Scatter(x=temp["Mês"], 
                    y=temp[subst],
                    text=round(temp[subst]).apply(lambda x: locale.currency(x, grouping=True,symbol=None)[:-3]),
                    mode='text',
                    textposition='top center',
                    textfont=dict(
                        size=12,
                    ),
                    showlegend=False,
                    hovertemplate='<extra></extra>'))
                
                fig.data[0].textfont.color = "white"
                fig.data[0].marker.color = "#9966ff"
                fig.data[1].marker.color = "#EBFF70"
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(title=None)
                #fig.update_traces(textposition="top center")
                st.plotly_chart(fig,use_container_width=True)
            except:
                fig = px.bar(
                    final2[(final2["data"]>= inc1) & (final2["data"]<= end1)],
                    x="Mês",
                    y=subst,
                    #color="Produtos",
                    #width=1000,
                    height=600,
                    text_auto='.2f',
                    title=f"Comissão Be.Smart Mensal",
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    labels = {subst:subst + "(R$)"}
                )
                fig.update_layout(
                    #showlegend=False,
                    legend_title= None,
                    uniformtext_minsize=8,
                    uniformtext_mode="hide",
                    legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    #xanchor="right",
                    #x=1
                    )
                    )
                fig.update_traces(textfont_size=12,textposition='inside')
                temp=final2[(final2["data"]>= inc1) & (final2["data"]<= end1)]
                temp=temp[['Mês',subst]].groupby('Mês').sum().reset_index()
                fig.add_trace(go.Scatter(x=temp["Mês"], 
                    y=temp[subst],
                    text=round(temp[subst]).apply(lambda x: locale.currency(x, grouping=True,symbol=None)[:-3]),
                    mode='text',
                    textposition='top center',
                    textfont=dict(
                        size=12,
                    ),
                    showlegend=False,
                    hovertemplate='<extra></extra>'))
                
                fig.data[0].textfont.color = "white"
                fig.data[0].marker.color = "#9966ff"
                fig.data[0]['showlegend']=True
                fig['data'][0]['name']=final2[(final2["data"]>= inc1) & (final2["data"]<= end1)]["Produtos"].iloc[0]
                #fig.data[1].marker.color = "#EBFF70"
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(title=None)
                #fig.update_traces(textposition="top center")
                st.plotly_chart(fig,use_container_width=True)
        

if st.button("Voltar"):
    nav_page("wide_project")

st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        div[data-testid="stSidebarNav"] {display: none;}
        footer {visibility: hidden;}
        div [data-testid="stToolbar"] {display: none;}
        [data-testid="collapsedControl"] {display: none}
        footer {visibility: hidden;}        
    </style>
""",
    unsafe_allow_html=True,
)




with open(r'style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#except:
    #nav_page('error')



