# Import Libraries
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc  # for styling

# 1. Load Data (Reusing Video 4's cleaned data)
try:
    df = pd.read_csv('doge_contracts.csv', parse_dates=['deleted_date'])
except FileNotFoundError:
    print("❌ Run Video #1's script to regenerate new data!")
    exit()

# 2. Create Standalone Plotly Chart
def save_top_vendors_chart():
    top_vendors = (df.groupby('vendor')['savings'].sum()
                  .nlargest(10).reset_index())
    
    fig = px.bar(
        top_vendors,
        x='vendor',
        y='savings',
        color='savings',
        title='Top 10 Vendors by Savings (Interactive)',
        labels={'savings': 'Total Savings (DOGE)'}
    )
    fig.write_html("top_vendors.html")

# 3. Build Dashboard App
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("DoGE Contracts Dashboard", 
                        className="text-center my-4"),
                width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='agency-dropdown',
                options=[{'label': ag, 'value': ag} 
                        for ag in sorted(df['agency'].unique())],
                placeholder="Select Agency..."
            )
        ], width=6),
        
        dbc.Col([
            dcc.DatePickerRange(
                id='date-range',
                min_date_allowed=df['deleted_date'].min(),
                max_date_allowed=df['deleted_date'].max(),
                start_date=df['deleted_date'].min(),
                end_date=df['deleted_date'].max()
            )
        ], width=6)
    ]),
    
    dcc.Graph(id='savings-plot')
], fluid=True)

# 4. Add Interactivity
@app.callback(
    Output('savings-plot', 'figure'),
    Input('agency-dropdown', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_chart(selected_agency, start_date, end_date):
    filtered = df.copy()
    if selected_agency:
        filtered = filtered[filtered['agency'] == selected_agency]
    filtered = filtered[(filtered['deleted_date'] >= start_date) & 
                       (filtered['deleted_date'] <= end_date)]
    
    return px.scatter(
        filtered,
        x='deleted_date',
        y='savings',
        color='vendor',
        hover_data=['description'],
        title=f"Savings Over Time ({selected_agency or 'All Agencies'})"
    )

if __name__ == '__main__':
    save_top_vendors_chart()  # Save standalone chart
    app.run(debug=True, port=8050)