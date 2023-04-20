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
from fastai.vision.all import *


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


@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(contents, filenames, dates):
    if contents is not None:
        children = [
            html.Div([
                html.H5(filename),
                html.H6(datetime.fromtimestamp(date)),
                html.Img(src=contents),
                html.Hr(),
                html.Div('Raw Content'),
                html.Pre(contents[0:200] + '...', style={
                    'whiteSpace': 'pre-wrap',
                    'wordBreak': 'break-all'
                })
            ])
            for contents, filename, date in zip(contents, filenames, dates)
        ]

        # Convert the first uploaded image to a PIL Image object
        first_image_pil = parse_contents(contents[0], filenames[0], dates[0])




    
        data = DataBlock(
          blocks=(ImageBlock, CategoryBlock),
          get_items=get_image_files,
          splitter=RandomSplitter(valid_pct=0.2, seed=42),
          get_y=parent_label,
          item_tfms=Resize(224)
          )

        dls = data.dataloaders( 'C:/Users/55449/Documents/GitHub/Arquivos/projeto/imagens')


        learn = vision_learner(dls, resnet34, metrics=error_rate)
        
        #learn.load("C:\Users\55449\Documents\GitHub\Arquivos\\projeto\\models\\modelo.pkl")
        learn = load_learner("C:/Users/55449/Documents/GitHub/Arquivos/projeto/modelo.pkl")
        
        
        
        
        img = PILImage.create(first_image_pil)
        pred, pred_idx, probs = learn.predict(img)
        
        return html.Div(children)

if __name__ == '__main__':
    app.run_server(debug=True)
