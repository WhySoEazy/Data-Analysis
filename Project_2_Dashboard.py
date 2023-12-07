import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output


us_counties = pd.read_csv('us-counties.csv' , encoding="ISO-8859-1")
us_counties['date'] = pd.to_datetime(us_counties.date, format='%Y-%m-%d')
us_counties.dropna(inplace=True)
us_counties['fips'] = us_counties['fips'].astype(int)

area = []
for i in range(1, 6):
    a = us_counties[us_counties['date'].dt.month == i]
    area.append(a['fips'].nunique())

deaths = []
for i in range(1, 6):
    a = us_counties[us_counties['date'].dt.month == i]
    deaths.append(a['deaths'].sum())

month = ['January', 'February', 'March', 'April', 'May']

colors = ['#94AAD6','#7388C1','#426EB4','#205AA7','#211551']

fig = go.Figure(data=go.Bar(x=month, y=area, marker_color=colors, width=0.3))
fig.update_layout( margin=dict(l=80, r=50, t=100, b=50),height=500,title='THE NUMBER OF COVID-19 INFECTED AREAS IN THE US THROUGH THE MONTHS',
                  xaxis_title='Month', yaxis_title='Number of Infected Areas',
                  xaxis=dict(tickfont=dict(size=12)), yaxis=dict(tickfont=dict(size=12)),
                  showlegend=False, font=dict(family='Georgia', size=12))

fig2 = go.Figure(data=go.Pie(labels=month, values=deaths,hole=0.6))
fig2.update_layout(margin=dict(l=50, r=80, t=100, b=80),height=500,title='COVID-19 DEATHS BY MONTH',
                   showlegend=True, font=dict(family='Georgia', size=12))

fig2.update_traces(marker=dict(colors=['#8DB4D8', '#274E72', '#6BB1C9', '#211551', '#448ACA']))

death_df= us_counties.groupby('date').agg(total_cases=('cases','sum'),total_deaths=('deaths','sum')).reset_index()
fig3 = go.Figure()

fig3.add_trace(go.Scatter(
    x=death_df['date'],
    y=death_df['total_cases'],
    mode='lines',
    name='Total Cases'
))

fig3.add_trace(go.Scatter(
    x=death_df['date'],
    y=death_df['total_deaths'],
    mode='lines',
    name='Total Deaths'
))

fig3.update_layout(
    title='Total COVID-19 Cases and Deaths over Time',
    xaxis_title='Date',
    yaxis_title='Count',
    xaxis=dict(tickangle=45),
    legend=dict(x=0.5, y=1.0, bgcolor='rgba(255, 255, 255, 0.5)'),
    font=dict(family='Georgia', size=13),
)

max_value = max(deaths)
font_colors = ['black' if value != max_value else '#DF0029' for value in deaths]
header = dict(values=['Month', 'Number of deaths due to Covid-19'],fill=dict(color=['#1B4F93', '#1B4F93']),font=dict(color='white'))
cells = dict(values=[month,deaths],font=dict(color=[font_colors, font_colors]))
table = go.Table(header=header, cells=cells)
fig4 = go.Figure(data=table)
fig4.update_layout(
    margin=dict(l=50, r=50, t=50, b=0),height=200,
    font=dict(family='Georgia', size=13))

max_value_2 = max(area)
font_colors_2 = ['black' if value != max_value_2 else '#DF0029' for value in area]
header = dict(values=['Month', 'Number of areas infected by Covid-19'],fill=dict(color=['#1B4F93', '#1B4F93']),font=dict(color='white'))
cells = dict(values=[month,area],font=dict(color=[font_colors_2, font_colors_2]))
table = go.Table(header=header, cells=cells)
fig5 = go.Figure(data=table)
fig5.update_layout(
    margin=dict(l=50, r=50, t=50, b=0), height=200,
    font=dict(family='Georgia', size=13))

top_flip_cases = us_counties.groupby('fips')['cases'].max().nlargest(10)
first_column = top_flip_cases.index
first_column_str = list(map(str, first_column))
second_column=top_flip_cases.values
fig6 = go.Figure(data=go.Bar(x=first_column_str, y=second_column, marker_color='#1B4F93', width=0.4))
fig6.update_layout( margin=dict(l=80, r=50, t=100, b=50),height=500,title='TOP 10 AREAS WITH THE MOST CASES OF COVID-19.',
                  xaxis_title='Month', yaxis_title='Number of Cases',
                  xaxis=dict(tickfont=dict(size=12)), yaxis=dict(tickfont=dict(size=12)),
                  showlegend=False, font=dict(family='Georgia', size=12))

top_flip_deaths = us_counties.groupby('fips')['deaths'].max().nlargest(10)
fcolumn = top_flip_deaths.index
fcolumn_str = list(map(str, fcolumn))
scolumn=top_flip_deaths.values
fig7 = go.Figure(data=go.Bar(x=fcolumn_str, y=scolumn, marker_color='#1B4F93', width=0.4))
fig7.update_layout( margin=dict(l=80, r=50, t=100, b=50),height=500,title='TOP 10 AREAS WITH THE MOST DEATHS OF COVID-19.',
                  xaxis_title='Month', yaxis_title='Number of Deaths',
                  xaxis=dict(tickfont=dict(size=12)), yaxis=dict(tickfont=dict(size=12)),
                  showlegend=False, font=dict(family='Georgia', size=12))

max_value_3 = max(second_column)
font_colors_3 = ['black' if value != max_value_3 else '#DF0029' for value in second_column]
county = []
state = []
for i in first_column:
    filtered_data = us_counties.loc[us_counties['fips'] == i]
    county_value = filtered_data['county'].values[0]
    county.append(county_value)
    state_value = filtered_data['state'].values[0]
    state.append(state_value)
header = dict(values=['Fips', 'County', 'State', 'Number of cases due to Covid-19'],
              fill=dict(color=['#1B4F93', '#1B4F93', '#1B4F93', '#1B4F93']), font=dict(color='white'))
cells = dict(values=[first_column_str, county, state, second_column],
             font=dict(color=[font_colors_3, font_colors_3, font_colors_3, font_colors_3]))
table = go.Table(header=header, cells=cells)
fig9 = go.Figure(data=table)
fig9.update_layout(
    margin=dict(l=50, r=50, t=0, b=0), height=250,
    font=dict(family='Georgia', size=13))

min_value = max(scolumn)
font_colors_4 = ['black' if value != min_value else '#DF0029' for value in scolumn]
county_min = []
state_min = []
for i in fcolumn:
    filtered_data = us_counties.loc[us_counties['fips'] == i]
    county_value = filtered_data['county'].values[0]
    county_min.append(county_value)
    state_value = filtered_data['state'].values[0]
    state_min.append(state_value)

header = dict(values=['Fips', 'County', 'State', 'Number of deaths due to Covid-19'],
              fill=dict(color=['#1B4F93', '#1B4F93', '#1B4F93', '#1B4F93']), font=dict(color='white'))
cells = dict(values=[fcolumn_str, county_min, state_min, scolumn],
             font=dict(color=[font_colors_4, font_colors_4, font_colors_4, font_colors_4]))
table = go.Table(header=header, cells=cells)
fig10 = go.Figure(data=table)
fig10.update_layout(
    margin=dict(l=50, r=50, t=0, b=0), height=250,
    font=dict(family='Georgia', size=13))

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    children=[
        html.H1('US COVID-19 DASHBOARD',
                style={'textAlign': 'center', 'font-family': 'Georgia', 'font-size': 50,'font-style': 'bold'}),
        html.P('(We write statistics based on a data table that records the number of cases and deaths of Covid 19 day by day from January to May 2020).',
               style={'textAlign': 'center', 'font-size': 15, 'font-style': 'italic'}),
        html.Div(
            className='row',
            style={'margin-bottom': '20px'},
            children=[
                html.Div(
                    className='col-6',
                    children=[
                        dcc.Graph(id='bar-chart', figure=fig)
                    ]
                ),
                html.Div(
                    className='col-6',
                    children=[
                        dcc.Graph(id='pie-chart', figure=fig2),

                    ]
                )
            ]
        ),
            html.Div(
            className='row',
            children=[
                html.Div(
                    className='col-6',
                    children=[
                        dcc.Graph(id='table-1', figure=fig5)
                    ]
                ),
                html.Div(
                    className='col-6',
                    children=[
                        dcc.Graph(id='table-2', figure=fig4),

                    ]
                )
            ]
        ),html.P('With the above chart, we can conclude that the number of affected areas and deaths due to Covid-19 from January to May shows signs of a strong increase, especially the outbreak in March and no sign of control.',
               style={'textAlign': 'center', 'font-size': 15,'font-family': 'Georgia'}),
         html.P('Although in May, the number of affected regions was the most. However, there was a decrease in the number of deaths due to the Covid-19 epidemic, from 651045 deaths to 244649, an significantly reduction.',
               style={'textAlign': 'center', 'font-size': 15, 'font-family': 'Georgia'}),
        dcc.Graph(figure=fig3),
        html.P('Here is a line chart that shows more clearly the dramatic change in the number of infections and deaths from the Covid-19 disease.',
               style={'textAlign': 'center', 'font-size': 15, 'font-family': 'Georgia'}),
        html.Div(
                    className='row',
                    children=[
                        html.Div(
                            className='col-6',
                            children=[
                                dcc.Graph(id='barchart-2', figure=fig6)
                            ]
                        ),
                        html.Div(
                            className='col-6',
                            children=[
                                dcc.Graph(id='barchart-3', figure=fig7),

                            ]
                        )
                    ]
                ),
        html.Div(
            className='row',
            children=[
                html.Div(
                    className='col-6',
                    children=[
                        dcc.Graph(id='table-3', figure=fig9)
                    ]
                ),
                html.Div(
                    className='col-6',
                    children=[
                        dcc.Graph(id='table-4', figure=fig10),

                    ]
                )
            ]
        ),
        html.P(''),
html.P(''),
        html.P('The top 10 locations with the greatest number of Covid-19 infections and fatalities are displayed in the graph above.',
               style={'textAlign': 'center', 'font-size': 15, 'font-family': 'Georgia'}),
        html.P('Cook County, Illinois, which has the FIPS code "17031," had the highest number of Covid-19 infections, with 43,255 cases.',
               style={'textAlign': 'center', 'font-size': 15, 'font-family': 'Georgia'}),
        html.P('In regard to Covid-19 deaths, Nassau County in the state of New York had the largest number of deaths (2250), according to FIPS code "36059".',
                style={'textAlign': 'center', 'font-size': 15, 'font-family': 'Georgia'}),
html.P(''),
html.P(''),
html.Div(["Input the State: ",dcc.Input(id='input-yr',value='New York',type='text',style={'height':'30px','font-size':20,'font-family': 'Georgia'}),
                                           ],
                                          style={'font-size':20,'font-family': 'Georgia','color': 'midnightblue'}),
                                 html.Br(),
                                 html.Br(),
                                 html.Div(dcc.Graph(id='bar-plot'))
    ]
)
@app.callback(Output(component_id='bar-plot',component_property='figure'),
              Input(component_id='input-yr',component_property='value'))
def get_graph(entered_year):
    death = us_counties[us_counties['state'] == entered_year]
    death_df = death.groupby('date').agg(total_cases=('cases', 'sum'),
                                               total_deaths=('deaths', 'sum')).reset_index()
    fig12 = go.Figure()

    fig12.add_trace(go.Scatter(
        x=death_df['date'],
        y=death_df['total_cases'],
        mode='lines',
        name='Total Cases'
    ))

    fig12.add_trace(go.Scatter(
        x=death_df['date'],
        y=death_df['total_deaths'],
        mode='lines',
        name='Total Deaths'
    ))

    fig12.update_layout(
        title='Total COVID-19 Cases and Deaths over Time in {}'.format(entered_year),
        xaxis_title='Date',
        yaxis_title='Count',
        xaxis=dict(tickangle=45),
        margin=dict(l=50, r=50, t=0, b=50),
        legend=dict(x=0.5, y=1.0, bgcolor='rgba(255, 255, 255, 0.5)'),
        font=dict(family='Georgia', size=13),
    )
    return fig12

if __name__ == '__main__':
    app.run_server()
