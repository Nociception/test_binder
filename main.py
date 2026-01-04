import duckdb
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -------------------------------
# 1. Génération des données
# -------------------------------
np.random.seed(42)
frames = []
n_points = 20  # nombre de points par frame
n_frames = 10

for t in range(n_frames):
    x = np.random.normal(loc=t, scale=1.0, size=n_points)
    y = np.random.normal(loc=t*0.5, scale=0.5, size=n_points)
    z = np.random.normal(loc=t*0.3, scale=0.2, size=n_points)
    frames.append(pd.DataFrame({
        'x': x,
        'y': y,
        'z': z,
        'time': t,
        'id': np.arange(n_points)  # identifiant du point pour traçage
    }))

df = pd.concat(frames, ignore_index=True)

# -------------------------------
# 2. Créer une mosaïque de subplots
# -------------------------------
fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=["X vs Y", "X vs Z", "Y vs Z"]
)

# -------------------------------
# 3. Créer les traces initiales (frame 0)
# -------------------------------
initial_frame = df[df['time'] == 0]

trace_xy = go.Scatter(
    x=initial_frame['x'],
    y=initial_frame['y'],
    mode='markers',
    marker=dict(size=10, color=initial_frame['id'], colorscale='Viridis', showscale=True),
    text=[f"ID: {i}" for i in initial_frame['id']],
    name='X vs Y'
)

trace_xz = go.Scatter(
    x=initial_frame['x'],
    y=initial_frame['z'],
    mode='markers',
    marker=dict(size=10, color=initial_frame['id'], colorscale='Viridis', showscale=False),
    text=[f"ID: {i}" for i in initial_frame['id']],
    name='X vs Z'
)

trace_yz = go.Scatter(
    x=initial_frame['y'],
    y=initial_frame['z'],
    mode='markers',
    marker=dict(size=10, color=initial_frame['id'], colorscale='Viridis', showscale=False),
    text=[f"ID: {i}" for i in initial_frame['id']],
    name='Y vs Z'
)

fig.add_trace(trace_xy, row=1, col=1)
fig.add_trace(trace_xz, row=1, col=2)
fig.add_trace(trace_yz, row=1, col=3)

# -------------------------------
# 4. Ajouter une zone de texte pour suivre un point
# -------------------------------
# Ici on suit le point d'id=5 par exemple
tracked_id = 5
tracked_point = initial_frame[initial_frame['id'] == tracked_id].iloc[0]

fig.add_annotation(
    x=tracked_point['x'], y=tracked_point['y'],
    xref='x1', yref='y1',
    text=f"Tracked ID: {tracked_id}",
    showarrow=True,
    arrowhead=2
)

# -------------------------------
# 5. Créer les frames d'animation
# -------------------------------
frames_list = []
for t in range(n_frames):
    df_t = df[df['time'] == t]
    tracked_point = df_t[df_t['id'] == tracked_id].iloc[0]

    frame = go.Frame(
        data=[
            go.Scatter(x=df_t['x'], y=df_t['y'], mode='markers', marker=dict(color=df_t['id'], colorscale='Viridis')),
            go.Scatter(x=df_t['x'], y=df_t['z'], mode='markers', marker=dict(color=df_t['id'], colorscale='Viridis')),
            go.Scatter(x=df_t['y'], y=df_t['z'], mode='markers', marker=dict(color=df_t['id'], colorscale='Viridis')),
        ],
        name=str(t),
        layout=go.Layout(
            annotations=[
                go.layout.Annotation(
                    x=tracked_point['x'], y=tracked_point['y'],
                    xref='x1', yref='y1',
                    text=f"Tracked ID: {tracked_id}",
                    showarrow=True,
                    arrowhead=2
                )
            ]
        )
    )
    frames_list.append(frame)

fig.frames = frames_list

# -------------------------------
# 6. Ajouter les boutons de lecture
# -------------------------------
fig.update_layout(
    updatemenus=[{
        "type": "buttons",
        "buttons": [
            {
                "label": "Play",
                "method": "animate",
                "args": [None, {"frame": {"duration": 500, "redraw": True},
                                "fromcurrent": True, "transition": {"duration": 0}}]
            },
            {
                "label": "Pause",
                "method": "animate",
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}]
            }
        ],
        "showactive": True,
    }]
)

# -------------------------------
# 7. Affichage
# -------------------------------
fig.update_layout(title="Mosaïque animée synchronisée avec suivi d'un point")
fig.write_html("subplot_animation_tracked.html", include_plotlyjs='cdn')
fig.show()
