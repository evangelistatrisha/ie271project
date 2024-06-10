from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
from urllib.parse import urlparse, parse_qs



from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.Div(
            [
                dcc.Store(id='propertiesprofile_toload', storage_type='memory', data=0)
            ]
        ),

        html.H2('Properties Details'), 
        html.Hr(),
        dbc.Alert(id='propertiesprofile_alert', is_open=False), 
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Property ID", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='propertiesprofile_propertyid',
                                placeholder="Property ID"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3' 
                ),
                dbc.Row(
                    [
                        dbc.Label("Item Name", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='propertiesprofile_itemname',
                                placeholder="Item Name"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3' 
                ),
                dbc.Row(
                    [
                        dbc.Label("Qty", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='propertiesprofile_qty',
                                placeholder="Qty"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3' 
                ),
                dbc.Row(
                    [
                        dbc.Label("Unit", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='propertiesprofile_unit',
                                placeholder="Unit"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3' 
                ),
                dbc.Row(
                    [
                        dbc.Label("Property Type", width=1),
                        dbc.Col(
                            dcc.Dropdown(
                                id='propertiesprofile_propertytype',
                                placeholder='Property Type'  
                            ),
                            width=5
                        )
                    ],
                    className='mb-3' 
                ),
                dbc.Row(
                    [
                        dbc.Label("Status", width=1),
                        dbc.Col(
                            dcc.Dropdown(
                                id='propertiesprofile_status',
                                placeholder='Status'
                            ),
                            width=5
                        )
                    ],
                    className='mb-3' 
                ), 
                dbc.Row(
                    [
                        dbc.Label("Employee ID", width=1),
                        dbc.Col(
                            dbc.Input(
                                type='text', 
                                id='propertiesprofile_employeeid',
                                placeholder="Employee ID"
                            ),
                            width=5
                        )
                    ],
                    className='mb-3' 
                ),               
                dbc.Row(
                    [
                        dbc.Label("Date Assigned", width=1),
                        dbc.Col(
                            dcc.DatePickerSingle(
                                id='propertiesprofile_dateassigned',
                                placeholder='Date Assigned',
                                month_format='YYYY-MM-DD',
                            ),
                            width=9
                        )
                    ],
                    className='mb-3'
                ),

            ]
        ),

        html.Div(
            dbc.Row(
                [
                    dbc.Label("Delete property?", width=2),
                    dbc.Col(
                        dbc.Checklist(
                            id='propertiesprofile_removerecord',
                            options = [
                                {
                                    'label': "Mark for deletion",
                                    'value': 1
                                }
                            ],
                            style={'fontWeight':'bold'},
                            
                        ),
                        width=6,
                    ),
                ],
                className="mb-3",
            ),
            id='propertiesprofile_removerecord_div'
        ),

          dbc.Button(
            'Submit',
            id='propertiesprofile_submit',
            n_clicks=0 
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    html.H4('Save Success!')
                ),
                dbc.ModalBody(
                    'The property details have been successfully updated.'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/properties' 
                    )
                )
            ],
            centered=True,
            id='propertiesprofile_successmodal',
            backdrop='static' 
        )
    ]
)


@app.callback(
    [
        Output('propertiesprofile_propertytype', 'options'),
        Output('propertiesprofile_status', 'options'),
        Output('propertiesprofile_toload', 'data'),
        Output('propertiesprofile_removerecord_div', 'style')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def propertiesprofile_loaddropdown(pathname, search):
    if pathname == '/properties/properties_profile':
        propertytype_sql = """
        SELECT distinct property_type as label, property_type as value
        FROM property
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(propertytype_sql, values, cols)  
        propertytype_options = df.to_dict('records')

        status_sql = """
        SELECT status as label, status as value
        FROM status
        """
        values = []
        cols = ['label', 'value']
        df = db.querydatafromdatabase(status_sql, values, cols)
        status_options = df.to_dict('records')

        parsed = urlparse(search)
        create_mode = parse_qs(parsed.query)['mode'][0]
        to_load = 1 if create_mode == 'edit' else 0

        removediv_style = {'display': 'none'} if not to_load else None

    else:
        raise PreventUpdate
    
    return [propertytype_options, status_options, to_load, removediv_style]


@app.callback(
    [
        
        Output('propertiesprofile_alert', 'color'),
        Output('propertiesprofile_alert', 'children'),
        Output('propertiesprofile_alert', 'is_open'),
        Output('propertiesprofile_successmodal', 'is_open')
    ],
    [
         
        Input('propertiesprofile_submit', 'n_clicks')
    ],
    [
        State('propertiesprofile_propertyid', 'value'),
        State('propertiesprofile_itemname', 'value'),
        State('propertiesprofile_qty', 'value'),
        State('propertiesprofile_unit', 'value'),
        State('propertiesprofile_propertytype', 'value'),
        State('propertiesprofile_status', 'value'),
        State('propertiesprofile_employeeid', 'value'),
        State('propertiesprofile_dateassigned', 'date'),
        State('url', 'search'),
        State('propertiesprofile_removerecord','value'),
    ]
)
def propertiesprofile_saveprofile(submitbtn, propertyid, itemname, qty, unit, propertytype, status, employeeid, dateassigned, search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'propertiesprofile_submit' and submitbtn:

            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            if not propertyid:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Property ID field is blank.'
            elif not itemname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Item name field is blank.'
            elif not qty:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Qty field is blank.'
            elif not unit:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Unit field is blank.'
            elif not propertytype:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Property type field is not selected.'
            elif not status:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Status field is not selected.'
            elif not employeeid:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Employee ID field is blank.'
            elif not dateassigned:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Input date is not selected.'
            else: 
                    
                    parsed = urlparse(search)
                    create_mode = parse_qs(parsed.query)['mode'][0]

                    if create_mode =='add':
                        
                        sql = '''
                            INSERT INTO property (property_id, item_name, qty, unit, property_type, status, employee_id, date_assigned, property_delete_ind)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            '''
                        values = [propertyid, itemname, qty, unit, propertytype, status, employeeid, dateassigned, False]
                        db.modifydatabase(sql, values)
                        modal_open = True
                                        
                    elif create_mode == 'edit':

                        parsed = urlparse(search)
                        propertyid = parse_qs(parsed.query)['id'][0]

                        
                        sqlcode = """ UPDATE property
                                SET
                                item_name = %s, 
                                qty = %s, 
                                unit = %s, 
                                property_type = %s, 
                                status = %s, 
                                employee_id = %s, 
                                date_assigned = %s,
                                property_delete_ind = %s
                                WHERE
                                property_id = %s
                            """
                        to_delete = bool(removerecord)

                        values = [itemname, qty, unit, propertytype, status, employeeid, dateassigned, to_delete, propertyid]
                        db.modifydatabase(sqlcode, values)

                        modal_open = True
                                    
            return [alert_color, alert_text, alert_open, modal_open]

        else:
            raise PreventUpdate

    else:
        raise PreventUpdate
    

@app.callback(
    [
        Output('propertiesprofile_propertyid', 'value'),
        Output('propertiesprofile_itemname', 'value'),
        Output('propertiesprofile_qty', 'value'),
        Output('propertiesprofile_unit', 'value'),
        Output('propertiesprofile_propertytype', 'value'),
        Output('propertiesprofile_status', 'value'),
        Output('propertiesprofile_employeeid', 'value'),
        Output('propertiesprofile_dateassigned', 'date'),
    ],
    [
        Input('propertiesprofile_toload', 'modified_timestamp')
    ],
    [
        State('propertiesprofile_toload', 'data'),
        State('url', 'search'),
    ]
)
def propertiesprofile_loadprofile(timestamp, toload, search):
    if toload: 
        
        
        parsed = urlparse(search)
        propertyid = parse_qs(parsed.query)['id'][0]

        
        sql = """
            SELECT property_id, item_name, qty, unit, property_type, status, employee_id, date_assigned
            FROM property
            WHERE property_id = %s
        """
        values = [propertyid]
        col = ['Property ID', 'Item Name', 'Qty', 'Property Type', 'Status', 'PIC-Official', 'Date Assigned']
        df = db.querydatafromdatabase(sql, values, col)

        
        propertyid = df['property_d'][0]
        itemname = df['itemname'][0]
        qty = int(df['qty'])[0]
        unit = df['unit'][0]
        propertytype = df['propertytype'][0]
        status = df['status'][0]
        employeeid = df['employeeid'][0]       
        dateassigned = df['releasedate'][0]

        return [propertyid, itemname, qty, unit, propertytype, status, employeeid, dateassigned]
        
    else:
        raise PreventUpdate
    