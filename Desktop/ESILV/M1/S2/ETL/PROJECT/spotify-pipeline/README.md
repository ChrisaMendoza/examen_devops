# 🎵 Spotify Trends Pipeline

Pipeline de données complet qui suit les tendances musicales mondiales en temps réel.

---

## Lancer le projet

### Étape 1 — Remplis tes clés Spotify dans le fichier .env
```
SPOTIFY_CLIENT_ID=f63b560e3fd94905be93e761ccee435c
SPOTIFY_CLIENT_SECRET=643963e0fad64dbc8bdf716fb6697ec6
```

### Étape 2 — Lance tous les services Docker
```bash
docker-compose up -d
```
Attends 5 minutes que tout démarre (Airflow installe ses dépendances).

### Étape 3 — Vérifie que tout tourne
```bash
docker ps
```
Tu dois voir 5 containers Up : postgres, zookeeper, kafka, airflow, streamlit.

### Étape 4 — Vérifie qu'Airflow est prêt
```bash
docker logs spotify_airflow --tail 5
```
Tu dois voir : "Listening at: http://0.0.0.0:8080"

### Étape 5 — Ouvre Airflow et lance le pipeline
- Va sur http://localhost:8080
- Login : admin / admin
- Cherche "spotify_pipeline", active-le et clique sur ▶️

### Étape 6 — Lance le consumer Kafka (nouveau terminal)
```bash
pip install kafka-python psycopg2-binary
python kafka/consumer.py
```

### Étape 7 — Regarde le dashboard
- Va sur http://localhost:8501

---

## Architecture
```
Spotify API → fetch_spotify.py → PostgreSQL staging
                                        ↓
                                   dbt models → PostgreSQL analytics
                                        ↓
                              producer.py → Kafka → consumer.py → live_feed
                                        ↓
                                 Streamlit Dashboard
                     (tout orchestré par Apache Airflow)
```
