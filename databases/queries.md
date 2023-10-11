Make sure you download the starter code and run the following:

```sh
  psql < movies.sql
  psql movies_db
```

In markdown, you can place a code block inside of three backticks (```) followed by the syntax highlighting you want, for example
\```sql

SELECT \* FROM users;

\```

Using the `movies_db` database, write the correct SQL queries for each of these tasks:

1.  The title of every movie.
SELECT title FROM movies;

2.  All information on the G-rated movies.
SELECT *
FROM movies 
WHERE rating LIKE 'G';

3.  The title and release year of every movie, ordered with the oldest movie first.
SELECT title, release_year
FROM movies
ORDER BY release_year;
    
4.  All information on the 5 longest movies.
SELECT *
FROM movies
WHERE runtime >=169;

5.  A query that returns the columns of `rating` and `total`, tabulating the
    total number of G, PG, PG-13, and R-rated movies.
SELECT rating,COUNT(*)
FROM movies
WHERE rating LIKE 'G',
rating LIKE 'PG',
rating LIKE 'PG-13',
rating LIKE 'R';

6.  A table with columns of `release_year` and `average_runtime`,
    tabulating the average runtime by year for every movie in the database. The data should be in reverse chronological order (i.e. the most recent year should be first).
SELECT release_year,AVG(runtime)
FROM movies;

7.  The movie title and studio name for every movie in the
    database.
SELECT title
FROM movies
UNION 
SELECT name
FROM studios;

8.  The star first name, star last name, and movie title for every
    matching movie and star pair in the database.
SELECT first_name,last_name
FROM starts
UNION 
SELECT *
FROM roles;


9.  The first and last names of every star who has been in a G-rated movie. The first and last name should appear only once for each star, even if they are in several G-rated movies. *IMPORTANT NOTE*: it's possible that there can be two *different* actors with the same name, so make sure your solution accounts for that.
SELECT first_name, last_name
FROM starts
UNION
FROM movies
WHERE rating LIKE 'G';


10. The first and last names of every star along with the number
    of movies they have been in, in descending order by the number of movies. (Similar to #9, make sure
    that two different actors with the same name are considered separately).

### The rest of these are bonuses
SELECT first_name, last_name
FROM stars 
UNION
SELECT AVG(movies)
FROM roles
ORDER BY DESC;

11. The title of every movie along with the number of stars in
    that movie, in descending order by the number of stars.
SELECT title
FROM movies
UNION 
SELECT AVG(start_id)
FROM roles

12. The first name, last name, and average runtime of the five
    stars whose movies have the longest average.
SELECT first_name, last_name, AVG(runtime)
FROM stars, movies 
WHERE runtime >= 168;

13. The first name, last name, and average runtime of the five
    stars whose movies have the longest average, among stars who have more than one movie in the database.
WITH MovieAvgRuntimes AS (
    SELECT
        s.first_name,
        s.last_name,
        AVG(m.runtime) AS avg_runtime
    FROM
        stars s
    JOIN
        stars_movies sm ON s.star_id = sm.star_id
    JOIN
        movies m ON sm.movie_id = m.movie_id
    GROUP BY
        s.first_name, s.last_name
    HAVING
        COUNT(sm.movie_id) > 1
)
SELECT
    first_name,
    last_name,
    avg_runtime
FROM
    (
        SELECT
            first_name,
            last_name,
            avg_runtime,
            RANK() OVER (ORDER BY avg_runtime DESC) AS ranking
        FROM
            MovieAvgRuntimes
    ) AS ranked_data
WHERE
    ranking <= 5;


14. The titles of all movies that don't feature any stars in our
    database.
SELECT m.title
FROM movies m
LEFT JOIN stars_movies sm ON m.movie_id = sm.movie_id
WHERE sm.movie_id IS NULL;

15. The first and last names of all stars that don't appear in any movies in our database.
SELECT s.first_name, s.last_name
FROM stars s
LEFT JOIN stars_movies sm ON s.star_id = sm.star_id
WHERE sm.star_id IS NULL;

16. The first names, last names, and titles corresponding to every
    role in the database, along with every movie title that doesn't have a star, and the first and last names of every star not in a movie.
SELECT s.first_name, s.last_name, r.title
FROM stars s
INNER JOIN roles r ON s.star_id = r.star_id


