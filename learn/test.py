a = "*"
print(a == '*')


import time as t

x = t.time()

for i in range(10):
  print(t.time()-x)
  t.sleep(1)