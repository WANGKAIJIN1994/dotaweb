#coding=utf-8

import json
from functools import reduce
import types

class json2sql:

	def __init__(self,table):
		self.table = table
		file = open(table + '.json')
		self.obj = json.loads(file.read())
		file.close()

	def getSql(self,object=None):

		def tosql(obj):
			col = ''
			val = ''
			for k,v in obj.items():
				col += '`' + k + '`,'
				val += '\"' + v + '\",' if type(v) != type(1) and not v.isdigit() else str(v) + ','
			col = col[:-1]
			val = val[:-1]
			return 'INSERT INTO `%s` (%s) VALUES(%s);' % (self.table, col, val)

		if object is not None:
			string = reduce(lambda str,y:str + '\n' + y,map(tosql,self.obj[object]))

		else:
			string = reduce(lambda str,y:str + '\n' + y,map(tosql,self.obj))

		output = open('all.sql', 'a')
		output.write('\nDELETE FROM `%s`;\n' % self.table)
		output.writelines(string)
		output.close()




if __name__ == '__main__':

	output = open('all.sql', 'w')
	output.write('')
	output.close()

	abilities = json2sql('abilities')
	heroes = json2sql('heroes')
	items = json2sql('items')
	leaver = json2sql('leaver')
	lobbies = json2sql('lobbies')
	modes = json2sql('modes')
	regions = json2sql('regions')

	abilities.getSql('abilities')
	heroes.getSql('heroes')
	items.getSql('items')
	leaver.getSql()
	lobbies.getSql('lobbies')
	modes.getSql('modes')
	regions.getSql('regions')