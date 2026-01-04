import duckdb
import numpy as np
import pandas as pd
import plotly.express as px

# -------------------------------
# 1. Charger ou générer des données
# -------------------------------

# Exemple : création d'une table DuckDB en mémoire
con = duckdb.connect(database=':memory:')

# Génération de données fictives : 10 "frames" temporelles, 50 points par frame
np.random.seed(42)
frames = []
for t in range(10):
    x = np.random.normal(loc=t, scale=1.0, size=50)
    y = np.random.normal(loc=t*0.5, scale=0.5, size=50)
    frames.append(pd.DataFrame({
        'x': x,
        'y': y,
        'time': t
    }))

df = pd.concat(frames, ignore_index=True)

# On peut stocker ça dans DuckDB
con.execute("CREATE TABLE points AS SELECT * FROM df")

# -------------------------------
# 2. Récupérer les données via DuckDB
# -------------------------------

# Exemple : filtrer ou calculer quelque chose via SQL
query = """
SELECT *, 
       x + y AS x_plus_y
FROM points
WHERE x_plus_y < 20
"""
df_sql = con.execute(query).fetchdf()

# -------------------------------
# 3. Préparer des transformations avec NumPy
# -------------------------------

# Par exemple : normalisation des colonnes pour l'affichage
df_sql['x_norm'] = (df_sql['x'] - df_sql['x'].mean()) / df_sql['x'].std()
df_sql['y_norm'] = (df_sql['y'] - df_sql['y'].mean()) / df_sql['y'].std()

# -------------------------------
# 4. Créer un nuage de points interactif avec Plotly
# -------------------------------

fig = px.scatter(
    df_sql,
    x='x_norm',
    y='y_norm',
    animation_frame='time',   # <- clé pour l'animation
    hover_data=['x', 'y'],   # hover show original values
    title="Nuage de points animé avec DuckDB, NumPy et Plotly",
    labels={'x_norm': 'X normalisé', 'y_norm': 'Y normalisé'}
)

# Options pour rendre l'animation plus "smooth"
fig.update_layout(
    transition={'duration': 500},
    xaxis=dict(range=[-3, 3]),
    yaxis=dict(range=[-3, 3])
)

# -------------------------------
# 5. Affichage web-friendly
# -------------------------------
# Dans Jupyter Notebook :
fig.show()

# Ou export en HTML autonome pour partager avec un recruteur :
fig.write_html("scatter_animation.html", include_plotlyjs='cdn')
