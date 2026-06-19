
  
    

  create  table "spotify_db"."analytics"."mart_top_tracks__dbt_tmp"
  
  
    as
  
  (
    WITH ranked AS (
    SELECT
        fetch_date,
        country,
        track_name,
        artist_name,
        popularity,
        ROW_NUMBER() OVER (PARTITION BY country, fetch_date ORDER BY popularity DESC) AS rank
    FROM "spotify_db"."analytics"."stg_tracks"
)
SELECT *
FROM ranked
WHERE rank <= 10
ORDER BY fetch_date DESC, country, rank
  );
  