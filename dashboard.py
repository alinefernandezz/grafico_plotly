import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

#Esta linha le o arquivo excel e armazena os dados numa variável chamad df
df = pd.read_excel('impacto_qualidade_ar.xlsx')


app = dash.Dash(__name__)

#layout
app.layout = html.Div([
    html.H1("Impacto da Poluição na Qualidade do Ar"),
    
    #selecionar poluente
    dcc.Dropdown(
        id='poluente-dropdown',
        options=[
            {'label': 'PM2.5', 'value': 'Concentração de PM2.5'},
            {'label': 'NO2', 'value': 'Concentração de NO2'}
        ],
        value='Concentração de PM2.5',
        clearable=False
    ),
    
    # grafico mapa
    dcc.Graph(id='mapa-poluicao'),
    
    # grafico linha
    dcc.Graph(id='grafico-poluição-tempo')
])

# callback para atualizar o mapa
@app.callback(
    Output('mapa-poluicao', 'figure'),
    [Input('poluente-dropdown', 'value')]
)
def atualizar_mapa(poluente_selecionado):
    fig = px.scatter_mapbox(
        df, lat="Latitude", lon="Longitude", hover_name="Região",
        hover_data=["Concentração de PM2.5", "Concentração de NO2", "População"],
        color=poluente_selecionado, size=poluente_selecionado,
        color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10
    )
    
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig

# atualizar o gráfico de linha
@app.callback(
    Output('grafico-poluição-tempo', 'figure'),
    [Input('poluente-dropdown', 'value')]
)
def atualizar_grafico(poluente_selecionado):
    fig = px.line(df, x='Data', y=poluente_selecionado, title=f'Tendência de {poluente_selecionado} ao longo do tempo')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
