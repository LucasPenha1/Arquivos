from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel("Vendas.xlsx")
#criando o gráfico
fig_1 = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
fig_2 = px.bar(df, x="ID Loja", y="Quantidade", color="Produto", barmode="group")
opcoes = list(df["ID Loja"].unique())
opcoes.append("Todas as Lojas")
app.layout = html.Div(children=[
    html.H1(children='Faturamento das Lojas'),
    html.H2(children="Gráfico com o faturamento de todos os produtos separados por loja"),
    html.Div(children='''
        Obs: Esse gráfico mostra a quantidade de produtos vendidos, não faturamento.
    ''',id="texto"),
    dcc.Dropdown(opcoes, value ='Todas as Lojas', id='lista_lojas'),
    dcc.Graph(
        id='grafico_quatidade_de_vendas',
        figure=fig_1
    ),
    dcc.Graph(
        id='example-graph',
        figure=fig_2
    )
])


@app.callback(
    Output('grafico_quatidade_de_vendas', 'figure'),
    Input('lista_lojas', 'value')
)
def update_output(value):
   if value == 'Todas as Lojas':
       fig_1 = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
   else:
       tabela_filtrada = df.loc[df["ID Loja"]==value, :]
       fig_1 = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
   return fig_1
if __name__ == '__main__':
    app.run_server(debug=True)