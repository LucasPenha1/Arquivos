import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

def dataFrame():
    df = pd.read_csv('C://Users//55449//Documents//GitHub//ProjetoRLX//nubank//nubank.csv')
    df.drop(df.loc[df['category'].isnull()].index, inplace=True)
    return df

def fig_categoria(df):
    fig = px.pie(df, values='amount', names='category', title='Population of European continent')
    return fig
def fig_date(df):
    fig = px.bar(df, x="date", y= 'amount',   barmode="group", title="Long-Form Input")
    return fig
def fig_title(df):
    fig = px.bar(df, x="title", y= 'amount',   barmode="group", title="Long-Form Input",text_auto='.2s',)
    return fig

app = Dash(__name__)

opcoes = ['Gasto por categoria','Gasto por data','Gasto por produto', 'Todos gastos']
app.layout = html.Div(children=[
    html.H1(children='TITULO'),
    html.Div(children='''
        Obs: OBSERVAÇÃO
    ''',id="texto"),
    dcc.Dropdown(opcoes, value = "Todos gastos", id='lista_gastos'),
    dcc.Graph(
        id='grafico_categoria'
    ),
    dcc.Graph(
        id='grafico_date'
    ),
    dcc.Graph(
        id='grafico_title'
    )
])


@app.callback(
    [Output('grafico_categoria', 'figure'), Output('grafico_date', 'figure'), Output('grafico_title', 'figure')],
  [ Input('lista_gastos', 'value')], prevent_initial_call=True
)
def update_output_1(value):
    df = dataFrame()
    if value == 'Gasto por categoria':
         return  fig_categoria(df), None, None
    elif value == 'Gasto por data':
        return fig_date(df), None, None
    elif value == 'Gasto por produto':
        return fig_title(df), None, None
    elif value == 'Todos gastos':
        return fig_date(df), fig_title(df), fig_categoria(df)
    return fig_date(df), fig_title(df), fig_categoria(df)
if __name__ == '__main__':
    app.run_server(debug=True)