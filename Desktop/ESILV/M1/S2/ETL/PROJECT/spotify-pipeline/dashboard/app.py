"""
app.py
Dashboard Streamlit pour visualiser les tendances musicales Spotify.
Se connecte à PostgreSQL via localhost (Docker expose le port 5432).
"""

import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Spotify Trends", page_icon="🎵", layout="wide")
st.title("🎵 Spotify Global Trends")
st.caption("Données mises à jour toutes les heures via le pipeline Airflow")


def load(query):
    conn = psycopg2.connect(
        host="postgres",
        dbname="spotify_db",
        user="spotify",
        password="spotify123",
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df


country = st.selectbox("Choisir un pays", ["FR", "US", "JP", "BR", "GB"])

st.subheader("🏆 Top 10 par pays aujourd'hui")
df1 = load(f"""
    SELECT track_name, artist_name, popularity, rank
    FROM analytics.mart_top_tracks
    WHERE country = '{country}' AND fetch_date = CURRENT_DATE
    ORDER BY rank
""")
if not df1.empty:
    fig = px.bar(df1, x="popularity", y="track_name", orientation="h",
                 color="popularity", color_continuous_scale="Greens",
                 hover_data=["artist_name"], labels={"track_name": "", "popularity": "Popularité"})
    fig.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Lance le pipeline d'abord pour voir les données !")

st.subheader("📈 Artistes en progression")
df2 = load(f"""
    SELECT artist_name, momentum_score, pop_today
    FROM analytics.mart_artist_momentum
    WHERE country = '{country}'
    ORDER BY momentum_score DESC LIMIT 10
""")
if not df2.empty:
    fig2 = px.bar(df2, x="artist_name", y="momentum_score",
                  color="momentum_score", color_continuous_scale="RdYlGn",
                  labels={"artist_name": "Artiste", "momentum_score": "Progression"})
    fig2.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("🌍 Popularité moyenne par pays")
df3 = load("""
    SELECT country, ROUND(AVG(popularity), 1) AS avg_pop
    FROM staging.raw_tracks
    WHERE fetch_date = CURRENT_DATE
    GROUP BY country ORDER BY avg_pop DESC
""")
if not df3.empty:
    fig3 = px.bar(df3, x="country", y="avg_pop", color="avg_pop",
                  color_continuous_scale="Blues",
                  labels={"country": "Pays", "avg_pop": "Popularité moyenne"})
    fig3.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("🎤 Artistes les plus présents dans le Top 50")
df4 = load(f"""
    SELECT artist_name, nb_tracks_in_top50, avg_popularity
    FROM analytics.mart_top_artists
    WHERE country = '{country}' AND fetch_date = CURRENT_DATE
    ORDER BY nb_tracks_in_top50 DESC LIMIT 10
""")
if not df4.empty:
    fig4 = px.scatter(df4, x="nb_tracks_in_top50", y="avg_popularity",
                      text="artist_name", size="avg_popularity", color="avg_popularity",
                      color_continuous_scale="Purples",
                      labels={"nb_tracks_in_top50": "Tracks dans le Top 50", "avg_popularity": "Popularité moyenne"})
    fig4.update_traces(textposition="top center")
    fig4.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig4, use_container_width=True)

st.subheader("🔴 Flux live (via Kafka)")
df5 = load("""
    SELECT track_name, artist_name, country, popularity, received_at
    FROM analytics.live_feed
    ORDER BY received_at DESC LIMIT 20
""")
if not df5.empty:
    st.dataframe(df5, use_container_width=True)
else:
    st.info("Lance le consumer Kafka pour voir les données apparaître ici.")

st.markdown("---")
st.caption("🔄 Rafraîchissement automatique toutes les 10 secondes")
st.markdown("<meta http-equiv='refresh' content='10'>", unsafe_allow_html=True)
