# TODO
import sys
from cs50 import SQL

db = SQL("sqlite:///students.db")
rows = db.execute("select * from students where house = :house order by last , first",
                    house = sys.argv[1])

for row in rows:
  if len(row['middle']) >0:
    name = row['first'] + ' '+ row['middle'] + ' '+row['last']
  else:
    name = row['first'] + ' '+row['last']
  print (name+', born '+ str(row['birth']) )