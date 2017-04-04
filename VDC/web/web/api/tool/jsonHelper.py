import json

class RecursiveEncoder(json.JSONEncoder):
	def default(self, o):
		return o.__dict__

def RecursiveDumpObject(o):
	return json.dumps(o, cls=RecursiveEncoder)