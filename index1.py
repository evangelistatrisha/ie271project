from dash import dcc
from dash import html
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import webbrowser
from app import app
from apps import commonmodules as cm
from apps import dbconnect as db


from apps import home
from apps.property import properties_home, properties_profile
from apps.reports import report
from apps import login
from apps import signup


CONTENT_STYLE = {
    "margin-top": "1em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

server = app.server
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),
        dcc.Store(id='sessionlogout', data=True, storage_type='session'),
        dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        dcc.Store(id='currentrole', data=-1, storage_type='session'),
        html.Div(
            cm.navbar,
            id='navbar_div'
        ),

        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)

@app.callback(
    [
        Output('page-content', 'children'),
        Output('sessionlogout', 'data'),
        Output('navbar_div', 'className'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
    ]
)
def displaypage (pathname, sessionlogout, userid):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else: 
        raise PreventUpdate
    
    if eventid == 'url':
        if userid < 0:
            if pathname == '/':
                returnlayout = login.layout
            elif pathname =='/signup':
                returnlayout = signup.layout
            else:
                returnlayout = '404: request not found'

        else:
            if pathname == 'logout':
                returnlayout = login.layout
                sessionlogout = True

            elif pathname == '/' or pathname == '/home':
               returnlayout = home.layout

            elif pathname == '/properties':
                returnlayout = properties_home.layout

            elif pathname == '/properties/properties_profile':
                returnlayout = properties_profile.layout

            elif pathname == '/reports':
                returnlayout = report.layout

                    
        logout_conditions = [
            pathname in ['/', 'logout'],
            userid == -1,
            not userid
        ]
        sessionlogout = any(logout_conditions)

        navbar_classname = 'd-none' if sessionlogout else ''

        return [returnlayout, sessionlogout, navbar_classname]
    else:
            raise PreventUpdate
    
if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=False)