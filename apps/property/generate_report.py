from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
from urllib.parse import urlparse, parse_qs
from fpdf import FPDF



from app import app
from apps import dbconnect as db
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# From sql data
sql_report = """SELECT property_id, item_name, qty, unit, property_type, status, employee_id, date_assigned
                FROM property
                WHERE NOT property_delete_ind"""


values = []
cols = ['Property ID', 'Item Name', 'Qty', 'Property Type', 'Status', 'PIC-Official', 'Date Assigned']
df = pd.DataFrame(sql_report)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Province of Batangas', 0, 1, 'C')
        self.cell(0, 10, 'City of Sto. Tomas', 0, 1, 'C')
        self.cell(0, 10, 'Properties owned by Brgy. San Rafael', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def table(self, df):
        self.set_font('Arial', 'B', 12)
        col_width = self.epw / len(df.columns)  # distribute content evenly
        for col in df.columns:
            self.cell(col_width, 10, col, border=1)
        self.ln()
        self.set_font('Arial', '', 12)
        for row in df.itertuples(index=False):
            for item in row:
                self.cell(col_width, 10, str(item), border=1)
            self.ln()

pdf = PDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("Arial", size=12)

print("PDF generated successfully!")