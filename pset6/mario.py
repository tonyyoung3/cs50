n = 0

while True:
  n = input("Height:\n")
  if n.isdigit() == False:
    n = input("Height:\n")
  else :
    n = int(n)
    if n <1 or n >8:
      n = input("Height:\n")
    else :
      break;


count = 1

for i in range(n):
  for k in range(n-count):
    print(" " , end = '')
  for j in range(count):
    print("#" , end = '')
  print("  " , end = '')
  for x in range(count):
    print("#" , end = '')
  print("")
  count += 1
