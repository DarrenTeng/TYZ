from api.vsphere import vsphere
from api.db import vmdb

def NewVM():
	vm = vsphere.CreateVM(VMName, templateName, guestAccount, guestPassword):
	if (vm is None):
		response = Response(True, "", "Create Failed", 1)
		return response.GetJson()

	if (vmdb.AddVM(vm.name, vm.uuid, vm.owner, vm.create_time, vm.guestAccount, vm.ip_address))
		vsphere.DeleteVM(vm)
		response = Response(True, "", "DB failed", 1)
		return response.GetJson()

	response = Response(False, vm, "Success", 1)
	return response.GetJson()


def DelVM():

def GetVMList():

def GetVMInfo():

