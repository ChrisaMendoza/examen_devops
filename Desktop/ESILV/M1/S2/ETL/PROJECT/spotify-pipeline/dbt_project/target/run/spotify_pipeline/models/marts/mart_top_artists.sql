
  
    

  create  table "spotify_db"."analytics"."mart_top_artists__dbt_tmp"
  
  
    as
  
  (
    SELECT
    fetch_date,
    country,
    artist_name,
    COUNT(DISTINCT track_id)   AS nb_tracks_in_top50,
    ROUND(AVG(popularity), 1)  AS avg_popularity
FROM "spotify_db"."analytics"."stg_tracks"
GROUP BY fetch_date, country, artist_name
ORDER BY fetch_date DESC, avg_popularity DESC
  );
  