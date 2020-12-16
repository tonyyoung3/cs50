# TODO
import csv
import sys
from cs50 import SQL

with open(sys.argv[1], newline='') as inputFile:
  db = SQL("sqlite:///students.db")
  rows = csv.reader(inputFile)

  for row in rows:
    name = row[0].split()
    house = row[1]
    birth = row[2]
    if(len(name) == 1):
      pass
    else:
      if(len(name)>2):
        first = name[0]
        middle = name[1]
        last = name[2]
      else:
        first = name[0]
        middle = ""
        last = name[1]
      rows = db.execute("select count(*) as id from students" )
      id = (rows[0]['id']) + 1

      db.execute("INSERT INTO students ( id, first, middle, last, house, birth) VALUES (:id,:first,:middle,:last,:house,:birth)" ,
                id = id , first =first , middle = middle,last = last,house = house, birth = birth)

