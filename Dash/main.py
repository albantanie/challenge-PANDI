from dash import Dash, dcc, html, dash_table, Input, Output, State
import base64
import io
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '90%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px auto'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload', style={'display': 'flex', 'flex-wrap': 'wrap'}),
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict('records')
        ),
        html.Div([
            dcc.Dropdown(
                id='filter-column',
                options=[{'label': i, 'value': i} for i in df.columns],
                value=df.columns[0]
            ),
            dcc.Graph(id='bar-chart'),
            dcc.Graph(id='pie-chart')
        ])
    ])

@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@app.callback(
    Output('bar-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Input('table', 'data'),
    Input('filter-column', 'value')
)
def update_graphs(rows, filter_column):
    df = pd.DataFrame(rows)
    filtered_df = df.groupby(filter_column).size().reset_index(name='count')

    bar_fig = px.bar(filtered_df, x=filter_column, y='count', title='Bar Chart')
    pie_fig = px.pie(filtered_df, names=filter_column, values='count', title='Pie Chart')

    return bar_fig, pie_fig

if __name__ == '__main__':
    app.run_server(debug=True)
