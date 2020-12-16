SELECT distinct a.name FROM "people" a inner join stars b on a.id = b.person_id inner join movies c on b.movie_id = c.id and c.year = 2004 ORDER BY birth
