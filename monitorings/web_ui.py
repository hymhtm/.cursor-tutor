from datetime import datetime, timedelta, timezone

from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd
from data_requests.request_logs import Requestlogs
from data_requests.config import settings
from dash_logging import logger

"""
Plot timeline graph using dash
    Args:
        df (pd.DataFrame): dataframe
        settings (settings): settings

    Returns:
        fig (plotly.graph_objects.Figure): graph
"""

#dash app initialization
app = Dash(__name__)

#layout setting
app.layout = html.Div(
    children=[
        html.H3(
            children='中村製作所',
            style = {'textAlign': 'right','font-size': '11px'}
        ),
        html.Div(
            id='title-and-time-display',
            children=[
                html.Div(children='稼働履歴',style={'font-size': '16px'}),
                html.Div(children=f'{(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d %H:%M")} ~ {datetime.now().strftime("%Y-%m-%d %H:%M")}',style={'font-size': '16px'})
            ],
            style={'marginBottom': '20px'}
        ),
        dcc.RadioItems(
            id='division-picker',
            options=[{'label': dep, 'value': dep} for dep in settings.department_dict.keys()],
            value='ALL',
            inline=True,
            style={'font-size': '16px'}
        ),
        dcc.Dropdown(
            id='equipment-dropdown',
            options=[{'label': equipment, 'value': equipment} for equipment in settings.department_dict['ALL']],
            value=settings.department_dict['ALL'],
            multi=True,
            placeholder='機械を選択',
            clearable=True,
            searchable=True
        ),
        dcc.Graph(
            id='timeline-graph',
            style={'width': '100%', 'height': '100vh'}
        ),
        dcc.Interval(
            id='interval-component',
            interval=5*60*1000, #5minutes
            n_intervals=0
        )
    ]
)

#callback setting
@callback(
    Output('equipment-dropdown', 'options'),
    Output('equipment-dropdown', 'value'),
    Input('division-picker', 'value'),
)

#select equipments by selected division
def update_equipment_options(selected_division):
    if selected_division:
        selected_equipments = settings.department_dict[selected_division]
        logger.debug(f'{selected_division}を選択, 設備：{selected_equipments}')
    else:
        selected_equipments = settings.department_dict['ALL']
        logger.debug(f'部門が選択されていません。すべての設備を使用します。')
    return selected_equipments, selected_equipments

@callback(
    Output('timeline-graph', 'figure'),
    Output('title-and-time-display', 'children'),
    Input('equipment-dropdown', 'value'),
    Input('interval-component', 'n_intervals'), #interval component is used to update graph on interval
)

#update graph on intervals
def update_graph(selected_equipments, n_intervals):
    print(datetime.now())
    if not selected_equipments:
        selected_equipments = settings.department_dict['ALL']
        logger.debug(f'設備が選択されていません。すべての設備を使用します。')
    
    requestlogs = Requestlogs(machine_groups={'ALL': selected_equipments})
    conditionlogs = requestlogs.request_condition_logs()
    df = requestlogs.format_logs(conditionlogs)
    
    begin_datetime = datetime.now(timezone(timedelta(hours=+9))) - timedelta(days=1)
    
    df_list = []
    
    for equipment_name, group_df in df.groupby('EquipmentName'):
        
        group_df = group_df.sort_values(by='StartDateTime')
        #print(group_df.iloc[0]['EquipmentName'], group_df.iloc[0]['StartDateTime'])
        if not group_df.empty and group_df.iloc[0]['StartDateTime'] <= begin_datetime:
            group_df.at[0, 'StartDateTime'] = begin_datetime
            #print(f'updated_value: {group_df.iloc[0]["StartDateTime"]}')
        df_list.append(group_df)
        
        df_clipped = pd.concat(df_list, ignore_index=True)
    print(df['EquipmentName'].unique())
    colors = settings.color_dict
    fig = px.timeline(df, x_start='StartDateTime', x_end='EndDateTime', y='EquipmentName', color='Contents', color_discrete_map=colors)
    fig.update_layout(title='稼働履歴', xaxis_title='時間', yaxis_title='機械名', legend_title='稼働内容', xaxis_range=[begin_datetime, datetime.now()])
    
    current_time_display = f'{(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d %H:%M")} ~ {datetime.now().strftime("%Y-%m-%d %H:%M")}'
    return fig, current_time_display

#app execution
if __name__ == '__main__':
    app.run_server(debug=True)