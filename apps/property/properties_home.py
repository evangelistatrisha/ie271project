from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
from urllib.parse import urlparse, parse_qs
from fpdf import FPDF
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime

from app import app

from apps import dbconnect as db


layout = html.Div(
    [   
        html.Div(
            [
                html.Img(src='/assets/Brgy-logo.png', style={'height':'100px', 'margin-right': '20px'}),
                html.H1('Properties owned by Brgy. San Rafael, Sto. Tomas City, Batangas', style={'display': 'inline-block', 'vertical-align': 'middle'}), 
            ],
            style={'display': 'flex', 'align-items': 'center'}
        ),
        html.Hr(),
        dbc.Card( 
            [
                dbc.CardHeader( 
                    [
                        html.H3('Manage Properties')
                    ]
                ),
                dbc.CardBody( 
                    [
                        html.Div( 
                            [
                                
                                dbc.Button(
                                    "Add Property",
                                    href='/properties/properties_profile?mode=add', 
                                    id='add-property', n_clicks=0
                                )
                            ]
                        ),
                        html.Br(),
                        html.Div( 
                             [
                                dbc.Button(
                                    "Generate Report File",
                                    id='generate_report', n_clicks=0
                                ),
                                dcc.Download(id="download-report")
                            ]
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.H4('Find Properties'),
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [
                                                dbc.Label("Search Item Name", width=2),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='propertieshome_itemnamefilter',
                                                        placeholder='Item Name'
                                                    ),
                                                    width=5
                                                )
                                            ],
                                            className='mb-3' 
                                        )
                                    )
                                ),
                                html.Div(
                                    "Table with item list will go here.",
                                    id='propertieshome_propertieslist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    [
        Output('propertieshome_propertieslist', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('propertieshome_itemnamefilter', 'value'), 
    ]
)
def propertieshome_loadpropertieslist(pathname, searchterm):
    print(pathname)
    if pathname == '/properties':
        sql = """ SELECT property_id, item_name, qty, property_type, status, employee_id, date_assigned
            FROM property 
            WHERE 
            NOT property_delete_ind
        """
        values = [] 
        cols = ['Property ID', 'Item Name', 'Qty', 'Property Type', 'Status', 'PIC-Official', 'Date Assigned']
        
        
        if searchterm:
            sql += " WHERE item_name ILIKE %s"
            
            values += [f"%{searchterm}%"]

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape[0] > 0:
            df['Qty'] = df['Qty'].apply(lambda x: f"{x:,}")
            df.style.set_properties(subset=['Qty'], align='right')
            df['Date Assigned'] = pd.to_datetime(df['Date Assigned']).dt.strftime('%d-%B-%Y')

            buttons =[]
            for property_id in df['Property ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'properties/properties_profile?mode=edit&id={property_id}',
                                   size='sm', color='warning'),
                                   style={'text-align':'center'}
                    )
                ] 

            df['Action'] = buttons

            status_color_map = {
                'Usable': 'green',
                'Assigned': 'blue',
                'Borrowed': 'orange',
                'Missing': 'red',
            }

            df['Status'] = df['Status'].apply(
                lambda status: html.Span(status, style={'color': status_color_map.get(status, 'black')})
            )

            table_header = [
                html.Thead(html.Tr([html.Th(col) for col in df.columns]))
            ]

            table_body = [
                html.Tbody([
                    html.Tr([
                        html.Td(row[col], style={'text-align': 'right'} if col == 'Qty' else {}) 
                        if col != 'Status' 
                        else html.Td(row[col]) 
                        for col in df.columns
                    ]) for _, row in df.iterrows()
                ])
            ]

            table = dbc.Table(table_header + table_body, striped=True, bordered=True, hover=True, size='sm')

            return [table]
        else:
            return ["No records to display"]
        
    else:
        raise PreventUpdate

def generate_pdf(data_frame, title):
    pdf_file = "Brgy. San Rafael-Property-Report.pdf"  # Save the file in the current working directory
    doc = SimpleDocTemplate(pdf_file, pagesize=landscape(A4),
                            rightMargin=0.5 * inch, leftMargin=0.5 * inch,
                            topMargin=0.5 * inch, bottomMargin=0.5 * inch)
    elements = []

    styles = getSampleStyleSheet()
    header_style = styles['Heading1']  
    centered_style = ParagraphStyle(name='CenteredText', alignment=1, parent=styles['Normal'])
    header_title_style = ParagraphStyle(name='HeaderTitle', alignment=1, fontSize=14, textColor=colors.black, fontName='Helvetica-Bold')

    
    current_date = datetime.now().strftime('%d-%B-%Y')
    title_lines = title.format(current_date=current_date).split("\n")
    
    for line in title_lines:
        centered_title = Paragraph(line, header_title_style)
        elements.append(centered_title)
        elements.append(Spacer(1, 0.1 * inch))
    elements.append(Spacer(1, 0.5 * inch))

    # Format for Qty
    data_frame['Qty'] = data_frame['Qty'].apply(lambda x: f"{x:,}")

    #color map for status
    status_color_map = {
        'Usable': colors.green,
        'Assigned': colors.blue,
        'Borrowed': colors.orange,
        'Missing': colors.red
    }

    
    header_row = [Paragraph(col, styles['Normal']) for col in data_frame.columns]
    data_rows = []

    for idx, row in data_frame.iterrows():
        data_row = []
        for col in data_frame.columns:
            if col == 'Status':
                status = row[col]
                color = status_color_map.get(status, colors.black)
                style = ParagraphStyle('StatusStyle', parent=styles['Normal'], textColor=color)
                data_row.append(Paragraph(str(status), style))
            elif col == 'Qty':
                style = ParagraphStyle('RightAlign', parent=styles['Normal'], alignment=2)
                data_row.append(Paragraph(str(row[col]), style))
            else:
                data_row.append(Paragraph(str(row[col]), styles['Normal']))
        data_rows.append(data_row)

    
    table_data = [header_row] + data_rows
    table = Table(table_data, repeatRows=1)
    
    
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (2, 1), (2, -1), 'RIGHT') 
    ])

    
    table.setStyle(style)
    
    
    col_widths = []
    for col in data_frame.columns:
        max_col_width = max([Paragraph(str(row[col]), styles['Normal']).wrap(doc.width, doc.height)[0] for idx, row in data_frame.iterrows()])
        col_width = max_col_width + 20  
        col_widths.append(col_width)

    
    total_width = sum(col_widths)
    available_width = doc.width
    if total_width > available_width:
        scale_factor = available_width / total_width
        col_widths = [w * scale_factor for w in col_widths]
    
    table._argW = col_widths
    
    elements.append(table)

    elements.append(Spacer(1, 0.5 * inch))  

    prepared_by = Paragraph("Prepared by:", styles['Normal'])
    verified_by = Paragraph("Verified by:", styles['Normal'])
    elements.append(prepared_by)
    elements.append(Spacer(1, 2 * inch)) 
    elements.append(verified_by)

    
    doc.build(elements)
    return pdf_file

@app.callback(
    Output("download-report", "data"),
    [Input("generate_report", "n_clicks")],
    [State('propertieshome_itemnamefilter', 'value')],
    prevent_initial_call=True
)
def download_report(n_clicks, searchterm):
    if n_clicks:
        sql = """ SELECT property_id, item_name, qty, property_type, status
            FROM property 
            WHERE 
            NOT property_delete_ind
        """
        values = []
        cols = ['Property ID', 'Item Name', 'Qty', 'Property Type', 'Status']

        if searchterm:
            sql += " AND item_name ILIKE %s"
            values += [f"%{searchterm}%"]

        df = db.querydatafromdatabase(sql, values, cols)

        if not df.empty:
            pdf_file = generate_pdf(df, "Province of Batangas\nCity of Sto. Tomas\nProperties Owned by Brgy. San Rafael\nAs of {current_date}")
            return dcc.send_file(pdf_file)
        else:
            raise PreventUpdate
        
if __name__ == "__main__":
    app.run_server(debug=True)