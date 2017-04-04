


def SignIn(username, password):
	user = UserDB.GetUserByName(username)
	if (user is None):
		Sleep(5000)
		response = Response(True, "", "User not exists", 1)
		return response.GetJson()

	if (user.CheckPassword(password) == False):
		Sleep(5000)
		response = Response(Ture, "", "Password not correct", 1)
		return response.GetJson()
	
	response = Response(False, user.type, "Successed", 1)
	

def SignUp():
	???

def SignOut():
	???

def ResetPwd():
	???