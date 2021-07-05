import plotly.graph_objects as go
import plotly.express as px

import numpy as np

import random, json, time, os

from KFHL_evaluate import KFHL_eval

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

with open("model/kfhl_names_index_pairs.json", "r") as read_file:
    PD = json.load(read_file)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.config.suppress_callback_exceptions = True


#################################################
################# Layout ########################
#################################################

app.layout = html.Div([

    
    html.H1(children='Super Simple KFHL Dash App'),
    html.H2(children='This is an example of a dash app that runs the KFHL model and displays the output as an interactive dashboard.'),
    
    html.H6("Change the value in the text box get a new plot"),
    html.Div(["     fII: ",
              dcc.Input(id='my-input-fii', value=1.0, type='number', debounce = True)]),
    html.Div(["      fV: ",
              dcc.Input(id='my-input-fv', value=1.0, type='number', debounce = True)]),
    html.Div(["   fVIII: ",
              dcc.Input(id='my-input-fviii', value=1.0, type='number', debounce = True)]),
    html.Br(),
     
    dcc.Graph(id='model-output'),

])

#####################
# Painter Vase Plot #
#####################
    
@app.callback(
    Output('model-output', 'figure'),
    [Input('my-input-fii', 'value'),
     Input('my-input-fv', 'value'),
     Input('my-input-fviii', 'value')])    
def make_plot(fii, fv, fviii):
        
    samples = np.ones(120) # Vector of all defaults
    samples[PD["Z8UP"]["index"]] = fviii  # Change Z8UP 
    samples[PD["Z2UP"]["index"]] = fii   # Change Z2UP (and Z2_INIT)
    samples[PD["Z5UP"]["index"]] = fv   # Change Z5UP (and Z5_INIT)
    
    start = time.time()
    totIIRZ = KFHL_eval(samples, 1200*100, 5.0, 0.5) 
    elapsed_time = time.time() - start
    #print("Elapsed time: %0.5f" % (time.clock() - start), "seconds")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.arange(1200), y=totIIRZ,
                    mode='lines',
                    name='KFHL Output'))
                    
    fig.update_yaxes(type="log", range=[-3,3])
    fig.update_layout(title="Model Output")
    
    return fig    
    
    
    
################
# Keyword Plot #
################

    
# -------------------------- MAIN ---------------------------- #


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
