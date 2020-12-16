import cs50 as cs
import math

count = 0;
n = round(cs.get_float("Change owed:") * 100)
if n < 0:
  n = round(cs.get_float("Change owed:") * 100)
else :

  while n >0 :
    if math.floor(n  / 25) > 0:
      count += math.floor(n / 25)
      n = n % 25
    elif math.floor(n  / 10) > 0:
      count += math.floor(n / 10)
      n = n % 10
    elif math.floor(n  / 5)  > 0:
      count += math.floor(n / 5)
      n = n % 5
    else :
      count += n
      n = 0
print(count);
