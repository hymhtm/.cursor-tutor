from datetime import datetime, timedelta

from dash import Dash, html, dcc, callback, callback_context, Input, Output
import plotly.express as px
import pandas as pd

from data_requests.request_logs import Requestlogs
from data_requests.config import settings

"""
Plot timeline graph using dash
    Args:
        df (pd.DataFrame): dataframe
        settings (settings): settings

    Returns:
        _type_: _description_
"""

#apiのデータ取得
logs = Requestlogs()
logs.begin_datetime = datetime.now()-timedelta(days=1)
logs.end_datetime = datetime.now()
condition_data = logs.request_condition_logs()

#dataframeの成型
df = logs.format_logs(condition_data)

#dataframeの期間算出
begin_datetime = df['StartDateTime'].min()
end_datetime = df['EndDateTime'].max()

#unixtimeの取得
begin_unixtime = int(begin_datetime.timestamp())
end_unixtime = int(end_datetime.timestamp())

#現在時刻の取得
current_time = datetime.now().strftime('%Y/%m/%d %H:%M')

#表示カラーの設定
colors = settings.color_dict
#dashの初期化
app = Dash(__name__)

#レイアウトの設定
app.layout = html.Div(
    children=[
        html.H3(children='中村製作所', style = {'textAlign': 'right','font-size': '11px'}),
        html.Div(
            children=[
                html.Div(children='稼働履歴',style={'font-size': '16px'}),
                html.Div(children=f'{begin_datetime} ~ {end_datetime}',style={'font-size': '16px'})
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
            options=[{'label': equipment, 'value': equipment} for equipment in df['EquipmentName'].unique()],
            value=df['EquipmentName'].unique(),
            multi=True,
            placeholder='機械を選択',
            clearable=True,
            searchable=True
        ),
        dcc.Graph(id='timeline-graph',style={'width': '100%', 'height': '100vh'})
    ]
)

#コールバックの設定
@callback(
    Output('timeline-graph', 'figure'),
    Output('equipment-dropdown', 'options'),
    Input('equipment-dropdown', 'value'),
    Input('division-picker', 'value')
)


#部門別のグラフ更新
def update_eqipments(selected_division):
    equipments = settings.department_dict.get(selected_division)
    return equipments

#グラフの更新
def update_graph(selected_equipments, selected_division):
    if selected_equipments is None:
        return {}
    else:
        filtered_df = df[
            df['EquipmentName'].isin(selected_equipments) 
        ].copy()
    fig = px.timeline(filtered_df, x_start='StartDateTime', x_end='EndDateTime', y='EquipmentName', color='Contents', color_discrete_map=colors)
    return fig

#アプリの実行
if __name__ == '__main__':
    app.run_server(debug=True)