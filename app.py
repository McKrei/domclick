import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Загрузка данных
data = pd.read_csv('real_estate_data.csv')

# Инициализация приложения Dash
app = dash.Dash(__name__)

# Определение списка регионов для выпадающего меню
regions = data['Регион'].unique()

# Определение метрик
metrics = [
    'Активных объявлений о продаже',
    'Активных объявлений, вторичка',
    'Активных объявлений, новостройки',
    'Средняя стоимость м², вторичка',
    'Средняя стоимость м², новостройки',
    'Средний срок экспозиции, вторичка'
]

# Константа для определения пиков и спадов
PERCENT_THRESHOLD = 0.03
IS_DEBUG = False

server = app.server  # Это нужно для Gunicorn

# Создание макета приложения
app.layout = html.Div([
    html.H1("Визуализация данных по недвижимости", style={'textAlign': 'center'}),
    html.Div([
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region, 'value': region} for region in regions],
            value=[regions[0]],
            multi=True,
            style={'width': '50%', 'display': 'inline-block', 'verticalAlign': 'middle'}
        ),
        html.Div(id='population-display', style={'width': '50%', 'display': 'inline-block', 'padding-left': '20px', 'font-size': '20px', 'verticalAlign': 'middle'})
    ], style={'textAlign': 'center', 'padding': '20px'}),
    html.Div([
        dcc.Checklist(
            id='toggle-peaks',
            options=[{'label': 'Показывать пики и спады', 'value': 'show'}],
            value=['show'],
            style={'textAlign': 'center', 'font-size': '20px'}
        )
    ], style={'textAlign': 'center', 'padding': '20px'}),
    html.Div(id='graphs-container', style={'padding': '0 20%'})
])

# Колбэк для обновления графиков и отображения населения
@app.callback(
    [Output('graphs-container', 'children'), Output('population-display', 'children')],
    [Input('region-dropdown', 'value'), Input('toggle-peaks', 'value')]
)
def update_graphs(selected_regions, toggle_peaks):
    if not selected_regions:
        return html.Div("Выберите хотя бы один регион."), ""

    graphs = []
    show_peaks = 'show' in toggle_peaks

    for metric in metrics:
        fig = px.line(title=f'{metric} по регионам', markers=True, labels={'value': metric, 'variable': 'Метрическая'})

        for region in selected_regions:
            filtered_data = data[data['Регион'] == region]
            fig.add_scatter(x=filtered_data['Дата'], y=filtered_data[metric], mode='lines+markers', name=region)

            if show_peaks:
                for i in range(1, len(filtered_data) - 1):
                    prev_value = filtered_data[metric].iloc[i - 1]
                    curr_value = filtered_data[metric].iloc[i]
                    next_value = filtered_data[metric].iloc[i + 1]

                    if (curr_value > prev_value * (1 + PERCENT_THRESHOLD)) and (curr_value > next_value * (1 + PERCENT_THRESHOLD)):
                        peak_value = curr_value
                        formatted_value = f'{peak_value:,.0f}'.replace(',', ' ')
                        fig.add_annotation(x=filtered_data['Дата'].iloc[i],
                                           y=peak_value,
                                           text=formatted_value,
                                           showarrow=True,
                                           arrowhead=1)
                    elif (curr_value < prev_value * (1 - PERCENT_THRESHOLD)) and (curr_value < next_value * (1 - PERCENT_THRESHOLD)):
                        trough_value = curr_value
                        formatted_value = f'{trough_value:,.0f}'.replace(',', ' ')
                        fig.add_annotation(x=filtered_data['Дата'].iloc[i],
                                           y=trough_value,
                                           text=formatted_value,
                                           showarrow=True,
                                           arrowhead=1,
                                           font=dict(color='red'),
                                           ax=0,
                                           ay=30)

        graphs.append(html.Div(dcc.Graph(figure=fig, config={
            'displaylogo': False,
        }), style={'width': '100%', 'padding-bottom': '20px'}))

    # Получение последнего значения населения для выбранных регионов
    latest_population = sum([data[data['Регион'] == region]['Население'].iloc[-1] for region in selected_regions])
    population_display = f"Общее население: {latest_population:,}".replace(',', ' ')

    return graphs, population_display

if __name__ == '__main__':
    app.run_server(debug=IS_DEBUG)
