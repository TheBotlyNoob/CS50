SELECT rating, title FROM movies
JOIN ratings ON movies.id=ratings.movie_id
WHERE year=2010 AND NOT rating LIKE '%N'
ORDER BY rating DESC, title ASC;