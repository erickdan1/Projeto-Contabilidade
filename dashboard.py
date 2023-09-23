import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
import json

import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

'''df = pd.read_excel('FINBRA_Estados-DF_Despesas_por_Função_2018-2021.xlsx', skiprows=4)

colunas_desejadas = ['Ano', 'UF', 'Coluna', 'Conta', 'Valor (R$)']

df_col_selecionadas = df[colunas_desejadas]

ld = ['08 - Assistência Social','09 - Previdência Social', '10 - Saúde']  # Deixar separado porque é o total das subfunções

linhas_desejadas = ['08.241 - Assistência ao Idoso',
                    '08.242 - Assistência ao Portador de Deficiência',
                    '08.243 - Assistência à Criança e ao Adolescente',
                    '08.244 - Assistência Comunitária',
                    '08.122 - Administração Geral',
                    'FU08 - Demais Subfunções',
                    '09.271 - Previdência Básica',
                    '09.272 - Previdência do Regime Estatutário',
                    '09.273 - Previdência Complementar',
                    '09.274 - Previdência Especial',
                    '09.122 - Administração Geral',
                    'FU09 - Demais Subfunções',
                    '10.301 - Atenção Básica',
                    '10.302 - Assistência Hospitalar e Ambulatorial',
                    '10.303 - Suporte Profilático e Terapêutico',
                    '10.304 - Vigilância Sanitária',
                    '10.305 - Vigilância Epidemiológica',
                    '10.306 - Alimentação e Nutrição',
                    '10.122 - Administração Geral',
                    'FU10 - Demais Subfunções']

lin_col_selecionadas = df_col_selecionadas['Conta'].isin(ld)

df_selecionado = df_col_selecionadas[lin_col_selecionadas]

df_selecionado.to_excel('df_seguridade_social.xlsx')
'''

df_seguridade_social = pd.read_excel("df_seguridade_social.xlsx")
df_seguridade_social_subfunc = pd.read_excel('df_seguridade_social_subfun.xlsx')

df_seguridade_social_RJ = df_seguridade_social[df_seguridade_social["UF"] == "RJ"]


# Como relacionar com os tipos de Despesas?
# Como vai ser esta comparação entre despesas
# Como fazer a sugestão do professor? --> Indicador de Execução (% de execução = Valor pago / Valor Empenhado * 100)
# Como implementar tabela deste dindicador de execução no dashboard?
# Como utilizar as subfunções?

# --------------------------------------------------
# instanciando dashboard
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

estados_brasil = json.load(open("geojson/brazil_geo.json", "r"))

fig = px.choropleth_mapbox(df_seguridade_social, locations="UF", color="Valor (R$)",
                           center={"lat": -16.95, "lon": -47.78}, range_color=(0, 443900912), zoom=4,
                           geojson=estados_brasil, color_continuous_scale="blues", opacity=0.6,
                           hover_data={"UF": True})

fig.update_layout(
    paper_bgcolor="#242424",
    autosize=True,
    margin=go.layout.Margin(l=0, r=0, t=0, b=0),
    showlegend=False,
    mapbox_style="carto-darkmatter"
)

fig2 = go.Figure(layout={"template": "plotly_dark"})
fig2.add_trace(go.Scatter(x=df_seguridade_social_RJ["Ano"], y=df_seguridade_social_RJ["Valor (R$)"]))
fig2.update_layout(paper_bgcolor="#242424",
                   plot_bgcolor="#242424",
                   autosize=True,
                   margin=dict(l=10, r=10, t=10, b=10))
# ---------------------------------------------------
# layout

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(id="logo", src=app.get_asset_url("logo_cin_bw.png"), height=50),
                html.H5("Análise de gastos com Seguridade Social no Brasil (2018-2021)"),
                dbc.Button("BRASIL", color="primary", id="location-button", size="lg")
            ], style={}),
            html.P("Informe o ano no qual deseja obter informações:", style={"margin-top": "40px"}),
            dcc.Dropdown(id="year-dropdown",
                         options=[{"label": "2018", "value": "2018"},
                                  {"label": "2019", "value": "2019"},
                                  {"label": "2020", "value": "2020"},
                                  {"label": "2021", "value": "2021"}]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Seguridade Social"),
                        html.H4(style={"color": "#FFD700"}, id="seguridade-social-text"),

                    ])
                ], color="light", outline=True, style={"margin-top": "10px",
                                                       "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px rgba(0, 0, 0, 0.19)",
                                                       "coloe": "#FFFFFF"})
            ], md=12)
        ]),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Assistência Social"),
                        html.H4(style={"color": "#adfc92"}, id="assistencia-social-text"),

                    ])
                ], color="light", outline=True, style={"margin-top": "10px",
                                                       "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px rgba(0, 0, 0, 0.19)",
                                                       "coloe": "#FFFFFF"})
            ], md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Previdência Social"),
                        html.H4(style={"color": "#389fd6"}, id="previdencia-social-text"),

                    ])
                ], color="light", outline=True, style={"margin-top": "10px",
                                                       "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px rgba(0, 0, 0, 0.19)",
                                                       "coloe": "#FFFFFF"})
            ], md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Span("Saúde"),
                        html.H4(style={"color": "#DF2935"}, id="saude-text"),

                    ])
                ], color="light", outline=True, style={"margin-top": "10px",
                                                       "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px rgba(0, 0, 0, 0.19)",
                                                       "coloe": "#FFFFFF"})
            ], md=4)
        ]),
            html.Div([
            html.P("Selecione a subfunção na qual deseja obter informações:", style={"margin-top": "25px"}),
            dcc.Dropdown(id="functions-dropdown",
                         options=[{"label": "Assistência Social", "value": "Conta"},
                                  {"label": "Previdência Social", "value": "Conta"},
                                  {"label": "Saúde", "value": "Conta"}]),
            dcc.Graph(id="linegraph", figure=fig2)
            ])

        ], md=6, style={"padding": "25px", "background-color": "#242424"}),


        dbc.Col([
            dcc.Loading(id="loading-1", type="default",
                        children=[
                            dcc.Graph(id="choropleth-map", figure=fig, style={"height": "100vh", "margin-right": "10px"})]
                        )

        ], md=6)
    ])


, fluid=True)

# ---------------------------------------
# Interatividade
@app.callback(
    [Output("seguridade-social-text", "children"), Output("assistencia-social-text", "children"),
     Output("previdencia-social-text", "children"),
     Output("saude-text", "children")],

    [Input("year-dropdown", "value"), Input("location-button", "children")]
)

def display_status(ano, location):
    if location == "BRASIL" and ano is None:
        df_data_on_year = df_seguridade_social
    elif location == "BRASIL" and ano is not None:
        df_data_on_year = df_seguridade_social[df_seguridade_social["Ano"].astype(str).str.contains(ano, case=False)]
    else:
        df_data_on_year = df_seguridade_social[
            (df_seguridade_social["UF"].astype(str).str.contains(location, case=False)) &
            (df_seguridade_social["Ano"].astype(str).str.contains(ano, case=False))
            ]

    seguridade_social = df_data_on_year["Valor (R$)"].sum()
    seguridade_social_format = locale.currency(seguridade_social, grouping=True)

    df_assistencia_social = df_data_on_year[df_data_on_year["Conta"].astype(str).str.contains("08 - Assistência Social", case=False)]
    assistencia_social = df_assistencia_social['Valor (R$)'].sum()
    assistencia_social_format = locale.currency(assistencia_social, grouping=True)

    df_previdencia_social = df_data_on_year[df_data_on_year["Conta"].astype(str).str.contains("09 - Previdência Social", case=False)]
    previdencia_social = df_previdencia_social['Valor (R$)'].sum()
    previdencia_social_format = locale.currency(previdencia_social, grouping=True)

    df_saude = df_data_on_year[df_data_on_year["Conta"].astype(str).str.contains("10 - Saúde", case=False)]
    saude = df_saude['Valor (R$)'].sum()
    saude_format = locale.currency(saude, grouping=True)

    return seguridade_social_format, assistencia_social_format, previdencia_social_format, saude_format

if __name__ == "__main__":
    app.run_server(debug=True)
