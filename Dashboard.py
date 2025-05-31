# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

# Get unique launch sites for dropdown
launch_sites = spacex_df['Launch Site'].unique()

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                
                                # TASK 1: Dropdown
                                dcc.Dropdown(id='site-dropdown',
                                           options=[{'label': 'All Sites', 'value': 'ALL'}] + 
                                                  [{'label': site, 'value': site} for site in launch_sites],
                                           value='ALL',
                                           placeholder="Select a Launch Site here",
                                           searchable=True),
                                html.Br(),

                                # TASK 2: Pie chart
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),

                                # TASK 3: Slider
                                dcc.RangeSlider(id='payload-slider',
                                              min=0,
                                              max=10000,
                                              step=1000,
                                              marks={i: str(i) for i in range(0, 11000, 1000)},
                                              value=[min_payload, max_payload]),

                                # TASK 4: Scatter chart
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2: Callback function
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, 
                    values=spacex_df.groupby('Launch Site')['class'].sum().values,
                    names=spacex_df.groupby('Launch Site')['class'].sum().index,
                    title='Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_failure_counts = filtered_df['class'].value_counts()
        fig = px.pie(values=success_failure_counts.values,
                    names=['Failed', 'Success'] if 0 in success_failure_counts.index else ['Success'],
                    title=f'Total Success Launches for site {entered_site}')
    return fig

# TASK 4 callback function
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_range):
    # Filter by payload range first
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, 
                        x='Payload Mass (kg)', 
                        y='class',
                        color='Booster Version Category',
                        title='Correlation between Payload and Success for all Sites')
    else:
        # Filter by specific site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df,
                        x='Payload Mass (kg)',
                        y='class', 
                        color='Booster Version Category',
                        title=f'Correlation between Payload and Success for site {entered_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run()