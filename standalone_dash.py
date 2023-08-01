import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objs as go

df = pd.read_csv("House_Rent_Dataset.csv")
cities = df["City"].value_counts()
label = cities.index
counts = cities.values
colors = ['gold', 'lightgreen']

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Pie Chart', value='tab-1'),
        dcc.Tab(label='Donut Chart', value='tab-2'),
        dcc.Tab(label='Histogram', value='tab-3'),
        dcc.Tab(label='Box Plot', value='tab-4'),
        dcc.Tab(label='Scatter Plot Graph', value='tab-5'),
        dcc.Tab(label='Bar Graph', value='tab-6'),
        dcc.Tab(label='Avg. Rent (Bar Graph)', value='tab-7'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(
    dash.dependencies.Output('tabs-content', 'children'),
    [dash.dependencies.Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H1(
                children='Pie Chart',
                style={
                    'textAlign': 'center'
                }
            ),
            html.Div(children='Different number of BHKs present in Houses available for Rent', style={
                'textAlign': 'center'
            }),
            dcc.Graph(
                figure=go.Figure(data=[go.Pie(labels=df['BHK'].value_counts().index, values=df['BHK'].value_counts().values)]),
                style={'height': '500px'}
            )
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H1(
                children='Donut Chart ',
                style={
                    'textAlign': 'center'
                }
            ),
            html.Div(children='Number of Houses Available for Rent in different Cities', style={
                'textAlign': 'center'
            }),
            dcc.Graph(
                figure=go.Figure(data=[go.Pie(labels=label, values=counts, hole=0.5)]),
                style={'height': '500px'}
            )
        ])
    elif tab == 'tab-3':
        fig_histogram = px.histogram(df, x="Size")
        return html.Div([
            html.H1(
                children='Histogram',
                style={
                    'textAlign': 'center'
                }
            ),
            html.Div(children='Size Distribution', style={
                'textAlign': 'center'
            }),
            dcc.Graph(
                figure=fig_histogram,
                style={'height': '500px'}
            )
        ])
    elif tab == 'tab-4':
        fig_box = px.box(df, x="Size")
        return html.Div([
            html.H1(
                children='BoxPlot',
                style={
                    'textAlign': 'center'
                }
            ),
            html.Div(children='Size Distribution', style={
                'textAlign': 'center'
            }),
            dcc.Graph(
                figure=fig_box,
                style={'height': '500px'}
            )
        ])
    elif tab == 'tab-5':
        fig_scatter = px.scatter(df, x='Size', y='Rent', color='BHK', size='Size', hover_data=['Rent'])
        fig_scatter.update_layout(
            yaxis_zeroline=False, xaxis_zeroline=False
        )
        return html.Div([
            html.H1(
                children='Scatter Plot Graph',
                style={
                    'textAlign': 'center'
                }
            ),
            html.Div(children='House Rent according to size and BHK of the house', style={
                'textAlign': 'center'
            }),
            dcc.Graph(
                figure=fig_scatter,
                style={'height': '500px'}
            )
        ])
    elif tab == 'tab-6':
        dropdown_options = [
            {'label': 'Size', 'value': 'Size'},
            {'label': 'BHK', 'value': 'BHK'},
            {'label': 'Furnishing Status', 'value': 'Furnishing Status'}
        ]
        dropdown_value = 'Size'
        figure_bar = px.bar(df, x=df["City"], y=df["Rent"], color=df[dropdown_value])
        return html.Div([
            html.H1(
                children='Bar Graph',
                style={
                    'textAlign': 'center'
                }
            ),
            html.Div(children='Rent in Different Cities According to Size, BHK, and Furnishing Status', style={
                'textAlign': 'center'
            }),
            dcc.Dropdown(
                id='bar-dropdown',
                options=dropdown_options,
                value=dropdown_value,
                style={'width': '200px', 'margin': 'auto', 'margin-top': '13px'},
                clearable=False  # Set clearable to False to prevent clearing the dropdown
            ),
            dcc.Graph(
                id='bar-graph',
                figure=figure_bar,
                style={'height': '500px','margin-top': '13px'}
            )
        ])
    elif tab == 'tab-7':
        avg_rent_df = df.groupby(['City', 'BHK'])['Rent'].mean().reset_index()
        figure_avg_rent = px.bar(avg_rent_df, x='City', y='Rent', color='BHK',
                                 labels={'Rent': 'Average Rent', 'BHK': 'Number of BHK'},)
                                #  title='Average House Rent in Different Cities by Number of BHK')

        return html.Div([
            html.H1(
                children='Average Rent (Bar Graph)',
                style={
                    'textAlign': 'center'
                }
            ),
            html.Div(children= 'Average House Rent in Different Cities by Number of BHK', style={
                'textAlign': 'center'
            }),
            dcc.Graph(
                figure=figure_avg_rent,
                style={'height': '500px', 'margin-top': '13px'}
            )
        ])

@app.callback(
    dash.dependencies.Output('bar-graph', 'figure'),
    [dash.dependencies.Input('bar-dropdown', 'value')]
)
def update_bar_graph(selected_value):
    if selected_value == 'Size':
        title = 'House Rent in Different Cities According to Size'
    elif selected_value == 'BHK':
        title = 'House Rent in Different Cities According to BHK'
    elif selected_value == 'Furnishing Status':
        title = 'House Rent in Different Cities According to Furnishing Status'
    else:
        title = ''

    figure_bar = px.bar(df, x=df["City"], y=df["Rent"], color=df[selected_value])
    figure_bar.update_layout(title=title)  #  title for the bar graph
    return figure_bar

if __name__ == "__main__":
    app.run_server(port=8050)  # Run the Dash app on port 8050
