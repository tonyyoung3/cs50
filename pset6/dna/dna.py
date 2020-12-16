import sys
import csv

f = open(sys.argv[2], newline='')
with open(sys.argv[1], newline='') as list:

  people = csv.reader(list)
  dnas = next(csv.reader(list))
  # print(dnas)

  # for person in people:
  #   print(person)

  dnas.pop(0)
  data = f.read()

  position = 0
  count = {}

  for dna in dnas:
    repeat = 0
    count[dna] = 0
    position = 0
    length = len(dna)
    # print(dna)

    while position < len(data):
      # print('p1')
      # print(position)
      x = data.find(dna,position) #0 ->55
      # print(x)
      if x >= 0: #find one or break
        repeat = 1
        # print('x length')
        # print(x + length)
        while data.find(dna, x + length) == x+length: #search next len(dna) letter to see if repeat
          x += length
          # if data.find(dna, x + length) >= 0:
          # print(x)
          repeat += 1

        # print('x')
        # print(x)
        position = x+length #finanl new position
        # print('p3')
        # print(position)
        if repeat > count[dna]:
          count[dna] = repeat
      else:
        break
  # print(count)
    #   print(position)




  final = 0

  for person in people:
    flag = 0
    # print(1)
    # print(person)
    for dna in dnas :
      # print(dna)
      # print (count[dna])
      # print (person[dnas.index(dna)+1])

      if int(count[dna]) != int(person[dnas.index(dna)+1]):
        flag = 1
    # print(flag)
    # print('------')
    if flag == 0:
      print(person[0])
      final = 1
  if final == 0 :
    print('No match')