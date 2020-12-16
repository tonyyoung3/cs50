select title from movies a
inner join stars b
on a.id = b.movie_id
inner join people c
on b.person_id = c.id and c.name = 'Chadwick Boseman'
inner join ratings d
on a.id = d.movie_id
order by d.rating desc
LIMIT 5