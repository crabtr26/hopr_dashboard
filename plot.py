import plotly.graph_objects as go
from plotly.subplots import make_subplots
from aggregate import load_tables


raw_df, weekday_df, hour_df, day_hour_df = load_tables()

TABLES = [weekday_df, hour_df, day_hour_df]
AGGS = ['Weekday', 'Hour', 'Weekday + Hour']
VALUES = ['Volume (HOPR)', 'Transaction Count']
MODES = ['Bar', 'Line']
AGG_TABLE = dict(zip(AGGS, TABLES))

COLORS = {
    'primary': '#F27405',
    'secondary': '#387CA6',
    'accent': '#22A2F2',
    'primary_text': '#0D0D0D',
    'secondary_text': '#595959',
    'accent_text': 'white',
    'primary_bg': '#F2F2F2',
    'secondary_bg': '#A6A6A6',
    'accent_bg': 'white',
    'grid': '#A6A6A6',
}


def generate_traces(df, key, value):
    '''
    Return a Bar, Line, and Marker trace for a given key, value pair in the df.
    The key will be the x-coord, the value will be the y-cord/title.
    '''
    traces = {
        'Bar': go.Bar( 
                x=df[key],
                y=df[value],
                text=df[value],
                name=value,
                texttemplate="%{text:.3s}",
                textposition='inside'
            ),
        'Line': go.Scatter(
                    x=df[key],
                    y=df[value],
                    text=df[value],
                    name=value,
                    mode='lines+markers'
                ),
    }

    return traces


def generate_axes_table():
    '''
    Generate a table of axis configurations.
    '''
    
    axes_table = {}

    for key in AGG_TABLE:

        ax_x = {
            'xaxis': {
                'showticklabels': True,
                'automargin': True,
                'gridcolor': COLORS['grid']
            }
        }
        axes_table[key] = ax_x

    for value in VALUES:

        ax_y = {
            'yaxis': {
                'title': {f'text': {value}, 'standoff': 25},
                'rangemode': 'tozero',
                'automargin': True,
                'gridcolor': COLORS['grid']
            }
        }
        axes_table[value] = ax_y
        
    return axes_table

def generate_figure_table():
    '''
    Generate a table of plotly figures. One for each choice of aggregation.
    Each choice has a bar plot and a line plot.
    '''
    def generate_figures(df, key, values):
        '''
        Generate a bar figure and a line figure for a specific aggregation.
        '''

        value1 = values[0]
        value2 = values[1]

        traces1 = generate_traces(df, key, value1)
        traces2 = generate_traces(df, key, value2)

        traces = [traces1, traces2]

        y1_range = [0.90*(df[value1].min()), 1.10*(df[value1].max())]
        y2_range = [0.90*(df[value2].min()), 1.10*(df[value2].max())]

        layout = go.Layout({
            'font': {'size': 12},
            'legend': {'title': {'text': 'Trading Indicator'}},
            'xaxis': {'showticklabels': True, 'automargin': True, 'gridcolor': COLORS['grid']},
            'xaxis2': {'showticklabels': True, 'automargin': True, 'gridcolor': COLORS['grid']},
            'yaxis': {'title': {'text': 'Volume (HOPR)', 'standoff': 25}, 'rangemode': 'tozero', 'automargin': True, 'gridcolor': COLORS['grid']},
            'yaxis2': {'title': {'text': 'Transaction Count', 'standoff': 25}, 'rangemode': 'tozero', 'automargin': True, 'gridcolor': COLORS['grid']},
            'autosize':True,

            ### Default Trace COLORS
            'colorway': [COLORS['primary'], COLORS['secondary']],

            ###
            'plot_bgcolor': COLORS['accent_bg'],

            ###
            'paper_bgcolor': COLORS['primary_bg'],

            'margin':dict(
                l=100,
                r=100,
                b=0,
                t=50,
                pad=0
            ),
        }) 

        barfig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=(f'{value1} by {key}', f'{value2} by {key}'))
        linefig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=(f'{value1} by {key}', f'{value2} by {key}'))

        for i, trace in enumerate(traces, start=1):
            barfig.add_trace(
                trace['Bar'],
                row=i,
                col=1
            )
            linefig.add_trace(
                trace['Line'],
                row=i,
                col=1
            )

        barfig.update_layout(layout)
        linefig.update_layout(layout)
        barfig = go.FigureWidget(barfig)
        linefig = go.FigureWidget(linefig)

        return barfig, linefig


    figure_table = {}

    for key in AGG_TABLE:
        agg_df = AGG_TABLE[key]
        barfig, linefig = generate_figures(agg_df, key=key, values=VALUES)
        entry = {
            'Bar': barfig,
            'Line': linefig,
        }
        figure_table[key] = entry
        
    return figure_table


if __name__ == '__main__':
    figure_table = generate_figure_table()
