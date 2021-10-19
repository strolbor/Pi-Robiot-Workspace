from json.decoder import JSONDecodeError
import types

class Strategie(object):

	def __init__(self,func=None):
		if func is not None:
			self.execute = types.MethodType(func,self)
			self.name = "{} @ {}".format(self.__class__.__name__, func.__name__)
		else:
			self.name = "{} default".format(self.__class__.__name__)
	
	def execute(self):
		print('Default method')
		print('{}\n'.format(self.name))

	def execute_replacement1(self):
		print('Replacement1 method')
		print('{} \n'.format(self.name))
	
	def execute_replacement2(self):
		print('Replacement2 method')
		print('Hallo: {} \n'.format(self.name))


print("S0")
s0 = Strategie()
s0.execute()

print("S1")
s1 = Strategie(Strategie.execute_replacement1)
s1.execute()

print("S2")
s1 = Strategie(Strategie.execute_replacement2)
s1.execute()

