import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objs as go
from app import app
from apps import dbconnect as db
from dash import dcc
from dash import html
from dash import dash_table
from dash.dash_table.Format import Group



layout = html.Div(
    [
        html.Div(
            [
                html.Img(src='/assets/Brgy-logo.png', style={'height':'100px', 'margin-right': '20px'}),
                html.H1('Reports', style={'display': 'inline-block', 'vertical-align': 'middle'}),
            ],
            style={'display': 'flex', 'align-items': 'center'}
        ),
        
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader(
                    [
                        html.H3('View Reports')
                    ]
                ),
                dbc.CardBody( 
                    [
                        html.Div(
                            [
                                html.Div(
                                    dbc.Form(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Label("Employee", width=1),
                                                    dbc.Col(
                                                        dcc.Dropdown(
                                                            id='report_picfilter',
                                                            placeholder='Select Employee ID',
                                                            searchable=True,
                                                            options = [],
                                                            multi = True
                                                        ),
                                                        width=5
                                                    )
                                                ], className = 'mb-3'
                                                
                                            ),
                                        ],
                                    )
                                ),
                                html.Div([
                                    dcc.Loading(
                                        id="reportbodyload",
                                        children=[
                                        dcc.Graph(id='reportbodyreceipts',)
                                      ],type="circle")
                                ],style={'width':'100%',"border": "3px #5c5c5c solid",} ),
                                html.Hr(),
                                html.H5('Number of Properties per PIC'),
                                html.Div(
                                    id='report_propertylist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


#callback to populate dropdown options
@app.callback(
    [
        Output('report_picfilter', 'options'),
        
    ],
    [
        Input('url', 'pathname'),
    ]
)
def propertyhome_loadpropertylist(pathname):
    if pathname == '/reports':
        sql = """
        SELECT DISTINCT e.employee_id as label, p.employee_id as value
        FROM employee as e
        LEFT JOIN property as p
        ON e.employee_id = p.employee_id
        WHERE p.property_delete_ind = %s
        """
        columns = ['label', 'value']
        values = [False]
        df = db.querydatafromdatabase(sql, values, columns)
        pic_options = df.to_dict('records')
    else:
        raise PreventUpdate
    return [pic_options]


#callback for figure and table
@app.callback(
    [
        Output('report_propertylist', 'children'),
        Output('reportbodyreceipts', 'figure')
    ],
    [
        Input('url', 'pathname'),
        Input('report_picfilter', 'value')
    ]
)
def propertyhome_loadpropertylist(pathname, filter_employee):
    if pathname == '/reports':
        sql = """ SELECT employee_id, count(item_name) as number_of_items, sum(qty) as total_qty
                FROM property
                WHERE property_delete_ind = False
            """
        values = []
        
        if filter_employee:
            sql += "AND employee_id IN %s"
            values += [tuple(filter_employee)]
        
        sql += """ Group By employee_id
                   Order By employee_id
        """

        cols = ['PIC-Official', 'Number of Items', 'Total Qty']

        df = db.querydatafromdatabase(sql, values, cols)
        
        traces = {

            'tracebar': go.Bar(
                y=df["Number of Items"],
                x=df["PIC-Official"],
                name='Number of Items'
            ),
        
         
            'traceline': go.Scatter(
                y=df["Total Qty"],
                x=df["PIC-Official"],
                mode= 'lines+markers',
                name='Total Qty',
                yaxis='y2'
            ) 
            
        }
              
        data=list(traces.values())

        
        layout = go.Layout(
                yaxis1={'title': "Number of Items"},
                yaxis2={'title': "Total Qty",'overlaying':'y','side':'right'},
                xaxis={'title': "PIC-Official"},
                height=500,
                width = 1000,
                margin={'b': 50,'t':20, 'l':175},
                hovermode='closest',
                autosize= False,
                dragmode = 'zoom',
                barmode='stack',
                boxmode= "overlay",
                )


        figure = {'data': data, 'layout': layout }
        

        table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                hover=True, size='sm')
        
        if df.shape[0]:
            return [table, figure]
        else:
            return ['No records to display', 'No figure to display']
    else:
        raise PreventUpdate