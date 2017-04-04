from tool.jsonHelper import RecursiveDumpObject

class Response:
	def __init__(self, error, data, message, time):
		self.error = error
		self.data = data
		self.message = message
		self.time = time
		pass

	def GetJson(self):
		return RecursiveDumpObject(self)


class TestData:
	def __init__(self, name, value):
		self.name = name
		self.value = value

def test():
	data = [TestData("name1", 1), TestData("name2", 2)]
	response = Response(True, data, "ErrorMessage", 123)
	ret = response.GetJson()
	if (ret == '{"message": "ErrorMessage", "time": 123, "data": [{"name": "name1", "value": 1}, {"name": "name2", "value": 2}], "error": true}'):
		print "Success"
	else:
		print "Failed" 

if (__name__ == '__main__'):
	test()

	