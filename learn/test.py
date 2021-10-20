import requests as re


a = "*"
print(a == '*')


import time as t

x = t.time()

for i in range(10):
  print(t.time()-x)



arr_a = ['a','B']

arr_b = ['a','B','c']

if arr_a in arr_b:
  print("Geht")

for entry in arr_a:
  for ent in arr_b:
    if entry == ent:
      print("gefunden",entry,ent)

d = re.post('http://192.168.1.104:5000/api/sendmail/Hallo Welt')
print(d)