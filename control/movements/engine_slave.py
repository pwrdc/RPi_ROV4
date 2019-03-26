import rov_comm
#import engine
import settings
import ast
import json


#engine_driver = engine.EngineDriver()
engine_slave = rov_comm.Client(settings.engine_slave_port)


while True:
	string = engine_slave.get_data()#.decode("utf-8") #robimy z byte na string
	string = string[2:-1] # i tak zostaje b"tekst", po tej instrukcji zostanie tekst
	dictionary = ast.literal_eval(string) #robimy dict
	print(dictionary)
	#engine_driver.set_engines(dictionary) #wrzucamy dict na silniki
