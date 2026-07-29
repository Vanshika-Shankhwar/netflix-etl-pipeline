-- =====================================================================
-- Netflix Titles: SQL Analytics
-- =====================================================================


-- ---------------------------------------------------------------------
-- Query 1: Top 3 genres per country, ranked by title count
-- ---------------------------------------------------------------------
WITH genre_counts AS (
    SELECT primary_country AS country,
           primary_genre AS genre,
           COUNT(*) AS title_count
    FROM titles
    WHERE primary_country != 'Unknown'
    GROUP BY primary_country, primary_genre
),
ranked AS (
    SELECT country, genre, title_count,
           RANK() OVER (PARTITION BY country ORDER BY title_count DESC) AS genre_rank
    FROM genre_counts
)
SELECT country, genre, title_count, genre_rank
FROM ranked
WHERE genre_rank <= 3
ORDER BY country, genre_rank;


-- ---------------------------------------------------------------------
-- Query 2: Year-over-year growth in titles added to Netflix
-- ---------------------------------------------------------------------
WITH yearly_additions AS (
    SELECT CAST(strftime('%Y', date_added) AS INTEGER) AS year_added,
           COUNT(*) AS titles_added
    FROM titles
    WHERE date_added IS NOT NULL
    GROUP BY year_added
)
SELECT year_added,
       titles_added,
       LAG(titles_added) OVER (ORDER BY year_added) AS prev_year_titles,
       ROUND(
           100.0 * (titles_added - LAG(titles_added) OVER (ORDER BY year_added))
           / LAG(titles_added) OVER (ORDER BY year_added), 1
       ) AS pct_change
FROM yearly_additions
ORDER BY year_added;


-- ---------------------------------------------------------------------
-- Query 3: Movie-to-TV Show ratio for the top 10 content-producing
-- ---------------------------------------------------------------------
WITH country_totals AS (
    SELECT primary_country AS country,
           SUM(CASE WHEN type = 'Movie' THEN 1 ELSE 0 END) AS movie_count,
           SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS tv_count,
           COUNT(*) AS total_titles
    FROM titles
    WHERE primary_country != 'Unknown'
    GROUP BY primary_country
)
SELECT country, movie_count, tv_count, total_titles,
       ROUND(1.0 * movie_count / NULLIF(tv_count, 0), 2) AS movie_to_tv_ratio
FROM country_totals
ORDER BY total_titles DESC
LIMIT 10;


-- ---------------------------------------------------------------------
-- Query 4: The oldest title in each genre
-- ---------------------------------------------------------------------
WITH ranked_titles AS (
    SELECT primary_genre AS genre, title, release_year,
           ROW_NUMBER() OVER (
               PARTITION BY primary_genre ORDER BY release_year ASC
           ) AS rn
    FROM titles
    WHERE primary_genre IS NOT NULL
)
SELECT genre, title, release_year
FROM ranked_titles
WHERE rn = 1
ORDER BY release_year ASC;


-- ---------------------------------------------------------------------
-- Query 5: Cumulative titles added to Netflix over time
-- ---------------------------------------------------------------------
WITH yearly_additions AS (
    SELECT CAST(strftime('%Y', date_added) AS INTEGER) AS year_added,
           COUNT(*) AS titles_added
    FROM titles
    WHERE date_added IS NOT NULL
    GROUP BY year_added
)
SELECT year_added,
       titles_added,
       SUM(titles_added) OVER (
           ORDER BY year_added ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS cumulative_titles
FROM yearly_additions
ORDER BY year_added;
