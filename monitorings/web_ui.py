from datetime import datetime

from dash import Dash, html, dcc, callback, Input, Output
import plotly.express as px
import pandas as pd

from data_requests.request_logs import Requestlogs
from data_requests.config import settings

"""
dashの練習用にタイムライングラフ作成

    Returns:
        _type_: _description_
"""

#dataframeの成型
df = pd.read_csv('C:/Users/nakamura114/Downloads/operation_result_20241213_100616.csv')
df['StartDateTime'] = pd.to_datetime(df['StartDateTime'])
df['EndDateTime'] = pd.to_datetime(df['EndDateTime'])

#dataframeの期間算出
begin_datetime = df['StartDateTime'].min()
end_datetime = df['EndDateTime'].max()

#unixtimeの取得
begin_unixtime = int(begin_datetime.timestamp())
end_unixtime = int(end_datetime.timestamp())

#現在時刻の取得
current_time = datetime.now().strftime('%Y/%m/%d %H:%M')

#表示カラーの設定
colors = {
    '運転中': 'green',
    '停止中': 'yellow',
    'アラーム中': 'red',
    '非常停止中': 'darkred',
    '一時停止中': 'orange',
    '手動運転中': 'blue',
    '切断中': 'gray',
    '待機中': 'blue',
    'Empty': 'lightgray'
}

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
            options=,
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
    Input('equipment-dropdown', 'value'),
    Input('division-picker', 'value')
)

#グラフの更新
def update_graph(selected_equipments, selected_division):
    if selected_equipments is None:
        return {}
    #start_time = datetime.fromtimestamp(selected_date_range[0])
    #end_time = datetime.fromtimestamp(selected_date_range[1])
    else:
        filtered_df = df[
            df['EquipmentName'].isin(selected_equipments) 
        ].copy()
    fig = px.timeline(filtered_df, x_start='StartDateTime', x_end='EndDateTime', y='EquipmentName', color='Contents', color_discrete_map=colors)
    return fig

#アプリの実行
if __name__ == '__main__':
    app.run_server(debug=True)