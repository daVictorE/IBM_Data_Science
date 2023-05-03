# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# install
# python3.8 -m pip install pandas dash
# wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# print(spacex_df)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                  dcc.Dropdown(id='site-dropdown',
                                    options = [{'label': 'All Sites', 'value': 'ALL'}] + 
                                        [{'label': i, 'value': i} for i in spacex_df['Launch Site'].unique()],
                                    value='ALL',
                                    placeholder="place holder here",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',
                                        2500: '2500',
                                        5000: '5000',
                                        7500: '7500',
                                        10000: '10000'},
                                    value=[1000, 9000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    # print(spacex_df.columns)
    filtered_df = spacex_df[['Launch Site', 'class']]
    filtered_df = filtered_df.groupby('Launch Site').sum().reset_index()
    
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names=filtered_df['Launch Site'], 
        title='Total Success Launches by Site')
        return fig
    else:
        df_site = spacex_df.loc[:, ['Launch Site', 'class']]
        filt = df_site['Launch Site']==entered_site
        sel_site = df_site[filt].groupby('class').count().reset_index()
        sel_site.columns = ['class', 'Outcomes']
        #print(sel_site)

        fig2 = px.pie(sel_site, 
            values='Outcomes', 
            names='class', 
            title=f'Total Success Launches for {entered_site}')
        return fig2
        # return the outcomes piechart for a selected site

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])
def get_scatter(entered_site, slider_range):
    print('get scatter-----------')
    print(spacex_df.columns)
    print(entered_site)

    sctr = spacex_df
    low, high = slider_range
    mask = (sctr['Payload Mass (kg)'] > low) & (sctr['Payload Mass (kg)'] < high)
    
    fsite = sctr['Launch Site'] == entered_site
    ent_site = sctr[fsite]

    if entered_site == 'ALL':
        fig3 = px.scatter(
            sctr[mask], 
            x='Payload Mass (kg)', 
            y='class', 
            color='Booster Version Category',
            title=entered_site)
        return fig3
    else:
        fig3 = px.scatter(
            ent_site[mask], 
            x='Payload Mass (kg)', 
            y='class', 
            color='Booster Version Category',
            title=entered_site)
        return fig3


# Run the app
if __name__ == '__main__':
    app.run_server()
