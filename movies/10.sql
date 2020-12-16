SELECT distinct a.name FROM "people" a
inner join directors b
on a.id = b.person_id
inner join movies c
on b.movie_id = c.id
inner join ratings d
on c.id = d.movie_id and d.rating >= 9
