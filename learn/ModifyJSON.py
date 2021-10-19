# -------------------------------------------------
# Json Modify String
import json

jsonStr = 'a|{"x": 241, "y": 212, "w": 53, "h": 134, "text": "bottle"}|{"x": 241, "y": 212, "w": 53, "h": 134, "text": "dsds"}'
print(jsonStr)
print("----")
splitter = jsonStr.split("|")
for a in splitter:
	print(a)
	try:
		aser = json.loads(a)
		if aser['text'] == 'bottle':
			print("Flasche gefunden")
			print("Auf x-Kordiante: ",aser['x']) 
	except JSONDecodeError:
		pass