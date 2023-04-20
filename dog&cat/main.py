import base64
import datetime
import io

import dash
import dash_html_components as html
import dash_core_components as dcc

from PIL import Image
import base64
import io
from dash.dependencies import Input, Output, State
from datetime import datetime

import tensorflow as tf
from PIL import Image
import numpy as np


app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-image-upload'),
])


def parse_contents(contents, filename, date):
    # decode base64 content string to bytes
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    # create PIL image object from bytes
    pil_image = Image.open(io.BytesIO(decoded))
    return pil_image


result = ''

def validation(first_image_pil):
    
        model = tf.keras.models.load_model('my_model.h5') 
        img = first_image_pil
        img = img.resize((224, 224))
# Converte a imagem em um array numpy e normaliza os valores dos pixels
        img_array = np.array(img) / 255.0
# Adiciona uma dimensão extra ao array numpy para que possa ser usado pelo modelo
        img_array = np.expand_dims(img_array, axis=0)
# Faz a previsão usando o modelo
        pred = model.predict(img_array)
######
        pred = np.argmax(pred,axis=1)
        if pred == [1]:
            result = "cão"
        elif pred == [0]:
            result = 'gato'
        return result

@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(contents, filenames, dates):
    if contents is not None:
        children = [
            html.Div([
                html.Img(src=contents),
                html.Hr()
            ])
            for contents, filename, date in zip(contents, filenames, dates)
        ]

        # Convert the first uploaded image to a PIL Image object
        first_image_pil = parse_contents(contents[0], filenames[0], dates[0])
        
    if contents is not None:
        children_1 = [
            html.Div([
                html.H1(validation(first_image_pil)),
             
            ])
        ]


        
        
        return html.Div(children),html.Div(children_1)

if __name__ == '__main__':
    app.run_server(debug=True)
