# Usual Dash dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd

# Let us import the app object in case we need to define
# callbacks here
from app import app
#for DB needs
from apps import dbconnect as db

@app.callback(
    [
        Output('propertiesprofile_propertytype', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)
def propertiesprofile_populatepropertytype(pathname):
    if pathname == '/properties/properties_profile':
        sql = """
        SELECT item_name as label, property_type as value
        FROM property 
        WHERE property_type_delete_ind = False
        """
        values = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, values, cols)
        

        propertytype_options = df.to_dict('records')
        print(df)
        return [propertytype_options]
    else:
        raise PreventUpdate