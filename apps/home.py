# Usual Dash dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output


from app import app
from apps import dbconnect as db


layout = html.Div(
    [
        html.Div(
            [
                html.Img(src='/assets/Brgy-logo.png', style={'height':'100px', 'margin-right': '20px'}),
                html.H1('Welcome to Brgy. San Rafael, Sto. Tomas City, Batangas!', style={'display': 'inline-block', 'vertical-align': 'middle'}),
            ],
            style={'display': 'flex', 'align-items': 'center'}
        ),
        html.Hr(),
        html.Div(
            [
                html.H4("Barangay Profile"),
                html.Br(),
                html.Br(),
                html.H5("Heyograpikong Lokasyon"),
                html.Br(),
                html.Span(
                    "Ang Barangay San Rafael ay isa sa tatlumpu na Barangay ng Lungsod ng Santo Tomas sa Probinsya ng Batangas. Ito ay matatagpuan sa hilagang bahagi ng nasabing bayan. Napapaligiran ito ng Barangay Sta. Anastacia sa bandang hilaga, Barangay Santiago sa bandang timog, Bundok Maria Makiling sa bandang silangan at Barangay Pantay, Lungsod ng Tanauan sa bandang kanluran."
                ),
                html.Br(),
                html.Br(),
                html.H5("Topograpiya"),
                html.Br(),
                html.Span(
                    "Ang Barangay San Rafael ay isang rural/patag na lugar sa mababang lupain, na may kabuuang sukat na 448.42 na hektarya."
                ),
                html.Br(),
                html.Br(),
                html.H5("Klima at Panahon"),
                html.Br(),
                html.Span(
                    "Gaya ng karamihan sa mga barangay sa Lungsod ng Santo Tomas, ang San Rafael ang karaniwang nakararanas ng Type 2 na uri ng klima kung saan walang tiyak na panahon ng tag-tuyot ngunit mayroong tiyak na panahon ng tag-ulan na karaniwang nagaganap mula Hunyo hanggang Disyembre ng taon."
                ),
                html.Br(),
                html.Br(),
                html.H5("Pang-edukasyon na Kalusugan at mga Pasilidad ng Serbisyo"),
                html.Br(),
                html.Span(
                    "Ang San Rafael ay mayroong isang pampublikong mababang paaralan na pinapakinabangan ng mga primary at intermediate na mag-aaral, na sa kasalukuyan ay may 1,779 na estudyante ang nakapagpatala at isang pampublikong mataas na paaralan na mayroon namng 2,734 na estudyante ang nakapagpatala, ito ang mga nakuhang datos na nakuha sa mga paaralan. Ang dalawang nasabing paaralan ay pawang pinangangasiwaan ng School District ng DepEd. Ang San Rafael ay mayroon ding dalawang Day Care Center na pinangangasiwaan naman ng mga may kasanayang Day Care Workers."
                ),
                html.Span(
                    "Ang Barangay ay maroon ding isang Health Center, labing lima (15) Barangay Health Workers, at tatlong (3) Barangay Nutrition Scholar na silang nagpapatupad at namamahala ng iba’t-ibang programa at serbisyong pangkalusugan kagaya nang maternal health care. Kabilang na rin dito ang mga serbisyo sa family planning, nutrisyon, at pagbabakuna sa mga batang may edad limang taon pababa."
                ),
                html.Br(),
                html.Br(),
                html.H5("Paraan ng Pampublikong Transportasyon"),
                html.Br(),
                html.Span(
                    "Ang pamahalaan ng Barangay San Rafael, na isang eco-industrial na barangay, ay patuloy na nagpapatupad ng mga gawaing imprastruktura, particular ang pagsasaayos ng mga road networks, upang mas mapadali ang panlupang paglalakbay. Mahigit ang pagpapatupad ng patas at pantay-pantay na pamasahe para sa mga pampasaherong sasakyan. Ang mga pinakakaraniwang pamamaraan ng pagbiyahe sa Barangay ay sa pamamagitan ng pampasaherong jeepney, mga motorsiklo at mga bus."
                ),
                html.Br(),
                html.Br(),
                html.H5("Mga Institusyon ng Pautang"),
                html.Br(),
                html.Span(
                    "Maraming institusyon na nagpapautang sa mga mamamayan ng barangay, ngunit wala silang opisina na matatagpuan sa barangay. Mayroon ding isa pang sektor na nagpapautang ng kapital sa mga negosyante ng barangay tulad ng CARD Bank at iba pa na kasalukuyang nag ooperate sa barangay ng ilang buwan o higit pa para sa mga miyembro nito."
                ),
                html.Br(),
                html.Br(),
                html.H5("Suplay ng Tubig at Elektrisidad"),
                html.Br(),
                html.Span(
                    "Mga protektadong bukal, pipe deep wells at koneksyon sa mga pribadong serbisyong patubig ang mga pinagkukunan ng inuming tubig ng mga taga-Barangay San Rafael. Para naman sa supply ng kuryente, 90% ng mga kabahayan ay kunektado sa Manila Electric Railroad Company."
                ),
                html.Br(),
                html.Br(),
                html.H5("Pamamahala ng Basura"),
                html.Br(),
                html.Span(
                    "Maraming institusyon na sa panahon ngayon, ang Barangay San Rafael ay may material recovery facility na maaaring gamitin sa pagtatapon ng mga basurang nakolekta sa barangay. Upang maisaayos ang mga basura sa barangay, regular itong hinahatak ng isang trak ng basura isang beses sa isang linggo."
                ),
                html.Br(),
                html.Br(),
                html.H5("Kapayapaan at Kaayusan"),
                html.Br(),
                html.Span(
                    "Ang Barangay San Rafael ay isa sa mga barangay na patuloy na nagpapatupad ng iba't ibang programa at estratehiya na nagpapanatili ng kaayusan at kapayapaan sa barangay. Regular na nagpapatrolya ang Barangay Tanod gabi at araw para sa kaligtasan ng mga residente. Aktibo rin ang barangay sa pagpapatupad ng Barangay Ordinance No.2, Barangay Curfew para sa mga kabataang labing walong (18) taong gulang pababa. Regular din ang pagpupulong ng pinuno ng peace and order committee minsan sa isang buwan upang makabuo ng mga plano para sa tamang pagpapatupad ng mga ordinansa at angkop na batas sa barangay."
                ),
                html.Br(),
                html.Br(),
                html.Hr(),
                html.Div(
                    [
                        html.H4('List of Barangay Officials'),
                    ]
                ),
                html.Hr(),
                html.Div(
                    [
                        html.Div(
                            dbc.Form(
                                dbc.Row(
                                    [
                                        dbc.Label("Search Barangay Official Name", width=2),
                                        dbc.Col(
                                            dbc.Input(
                                                type='text',
                                                id='home_employeenamefilter',
                                                placeholder='Name'
                                            ),
                                            width=5
                                        )
                                    ],
                                    className='mb-3' 
                                )
                            )
                        ),
                        html.Div(
                            id='home_employeelist'
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    [
        Output('home_employeelist', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('home_employeenamefilter', 'value'), 
    ]
)
def home_loademployeelist(pathname, searchterm):
    if pathname == '/home':
        sql = """ SELECT employee_name, position
            FROM employee
        """
        values = [] 
        cols = ['Name', 'Position']
        
        if searchterm:
            sql += "WHERE employee_name ILIKE %s"
            
            values += [f"%{searchterm}%"]

        df = db.querydatafromdatabase(sql, values, cols)
        
        if df.shape:            
            table = dbc.Table.from_dataframe(df, striped=True, borderless=True,
                    hover=True, responsive=True, size='sm')
            return [table]
        else:
            return ["No records to display"]
        
    else:
        raise PreventUpdate
