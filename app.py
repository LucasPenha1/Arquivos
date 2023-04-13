from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

#importando o bd
df = pd.read_csv('dados.csv',sep = ";", encoding='latin')
#excluindo colunas que não servirão para a analise de nota
df.drop(['Nº','Unnamed: 3','Unnamed: 5','Unnamed: 7','Unnamed: 9','Unnamed: 11','Unnamed: 13'], axis = 1, inplace = True)
df = df.drop(0)

materias = ['Matemática', 'Português', 'Química', 'Física','História', 'Biologia']
opcoes =  ['Matemática', 'Português', 'Química', 'Física','História', 'Biologia']
opcoes.append("Todas materias")
for coluna in materias:
    df[coluna] = df[coluna].astype(float)

df['Média'] = df.iloc[:, 1:7].sum(axis=1)/6

fig = px.bar(df, x="Nome do Aluno", y= materias,   barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Notas dos alunos'),
    html.Div(children='''
        Obs: Esse gráfico as notas dos alunos
    ''',id="texto"),
    dcc.Dropdown(opcoes, value = "Todas materias", id='lista_materias'),
    dcc.Graph(
        id='grafico_materias',
        figure=fig
    )
])


@app.callback(
    Output('grafico_materias', 'figure'),
    Input('lista_materias', 'value')
)
def update_output(value):
   if value == 'Todas materias':
       fig =  px.bar(df, x="Nome do Aluno", y= materias,   barmode="group")
   else:
       fig = px.bar(df, x="Nome do Aluno", y= value,   barmode="group")
   return fig





if __name__ == '__main__':
    app.run_server(debug=True)