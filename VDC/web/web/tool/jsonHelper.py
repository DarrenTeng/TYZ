import json

class RecursiveEncoder(json.JSONEncoder):
	def default(self, o):
		return o.__dict__

def RecursiveDumpObject(o):
	return json.dumps(o, cls=RecursiveEncoder)

class responseDataFormat:
    def __init__(self,result,data,error,time):
        self.result = result
        self.data = data
        self.error = error
        self.time = time
        pass
