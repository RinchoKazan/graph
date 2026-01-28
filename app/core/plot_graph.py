import plotly.graph_objects as go

def plot_graph(x, y, title="График", params=None):
    """
    params: словарь параметров, будет отображаться в легенде
    """
    fig = go.Figure()

    # Формируем название графика с параметрами
    name = title
    if params:
        params_str = ", ".join(f"{k}={v}" for k, v in params.items())
        name = f"{title} ({params_str})"

    # Добавляем интерактивные точки с hover
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines+markers',
        name=name,
        hovertemplate="X: %{x}<br>Y: %{y}<extra></extra>"
    ))

    fig.update_layout(
        title=title,
        xaxis_title="X",
        yaxis_title="Y",
        template="plotly_dark",
        autosize=True,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    # Авто-диапазон Y
    y_min, y_max = min(y), max(y)
    if y_min == y_max:
        y_min -= 1
        y_max += 1
    fig.update_yaxes(range=[y_min, y_max])

    return fig.to_html(full_html=False, include_plotlyjs='cdn')