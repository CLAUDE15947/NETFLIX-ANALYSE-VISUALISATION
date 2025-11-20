import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc


data_Netflix = pd.read_csv(r"C:\Users\jeanc\OneDrive\Documents\KAGGLE_VISUALISATION\Data_set\Netflix_cleaned.csv")


data_Netflix["date_added"] = pd.to_datetime(data_Netflix["date_added"], errors="coerce")


data_Netflix['duration'] = pd.to_numeric(data_Netflix['duration'], errors='coerce')


app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])


fig_type = px.pie(data_Netflix, names="type", title="Répartition Films / Séries")


df_country = (
    data_Netflix["country"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
    .value_counts()
    .head(15)
    .reset_index()
)
df_country.columns = ["country", "count"]
fig_country = px.bar(df_country, x="country", y="count", title="Top 15 des pays producteurs")


data_Netflix["year_added"] = data_Netflix["date_added"].dt.year
df_year = data_Netflix.groupby("year_added").size().reset_index(name="count")
fig_time = px.line(df_year, x="year_added", y="count", title="Évolution du nombre de contenus ajoutés")


df_genre = (
    data_Netflix["listed_in"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
    .value_counts()
    .head(15)
    .reset_index()
)
df_genre.columns = ["genre", "count"]
fig_genre = px.bar(df_genre, x="genre", y="count", title="Top 15 des genres Netflix")


df_movie = data_Netflix[data_Netflix["type"] == "Movie"]
fig_duration = px.histogram(df_movie, x="duration", nbins=40, title="Distribution des durées (films)")


df_rating = data_Netflix["rating"].value_counts().reset_index()
df_rating.columns = ["rating", "count"]
fig_rating = px.bar(df_rating, x="rating", y="count", title="Répartition des classifications d'âge")


df_delay = data_Netflix.copy()
df_delay["delay"] = df_delay["date_added"].dt.year - df_delay["release_year"]
fig_delay = px.histogram(df_delay, x="delay", nbins=40, title="Décalage sortie / ajout sur Netflix")

#
df_scatter = df_movie.dropna(subset=["duration", "release_year"])
fig_scatter = px.scatter(
    df_scatter,
    x="release_year",
    y="duration",
    color="rating",
    title="Nuage de points : Durée des films en fonction de l'année de sortie",
    labels={"release_year": "Année de sortie", "duration": "Durée (minutes)"}
)

app.layout = dbc.Container([
    html.H1(" Dashboard Netflix", className="text-center my-4"),

    dcc.Tabs([
        dcc.Tab(label=" Films vs Séries", children=[html.Br(), dcc.Graph(figure=fig_type)]),
        dcc.Tab(label=" Pays Producteurs", children=[html.Br(), dcc.Graph(figure=fig_country)]),
        dcc.Tab(label=" Évolution Temporelle", children=[html.Br(), dcc.Graph(figure=fig_time)]),
        dcc.Tab(label=" Genres", children=[html.Br(), dcc.Graph(figure=fig_genre)]),
        dcc.Tab(label=" Durées", children=[html.Br(), dcc.Graph(figure=fig_duration)]),
        dcc.Tab(label=" Ratings", children=[html.Br(), dcc.Graph(figure=fig_rating)]),
        dcc.Tab(label=" Décalage Sortie / Ajout", children=[html.Br(), dcc.Graph(figure=fig_delay)]),
        dcc.Tab(label=" Nuage de points", children=[html.Br(), dcc.Graph(figure=fig_scatter)]),
    ])
], fluid=True)


if __name__ == "__main__":
    app.run(debug=True)

