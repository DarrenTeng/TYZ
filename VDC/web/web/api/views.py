from datetime import datetime
from threading import Thread

from flask import request, session

from web.api.core.vcenter import get_task_id, do_new_vm, VCenter
from web.modules import VMList
from web.tool.jsonHelper import responseDataFormat, RecursiveDumpObject
from . import api
from web.api.core.virtualmachine import VirtualMachine
import random

os_list = [
    {"name": "Windows 10 Enterprise 64-bit", "value": "Windows_10_Ent_x64"},
    {"name": "Windows 10 Enterprise 32-bit", "value": "Windows_10_Ent_x86"},
    {"name": "Windows 8.1 Enterprise 64-bit", "value": "Windows_81_Ent_x64"},
    {"name": "Windows 8.1 Enterprise 32-bit", "value": "Windows_81_Ent_x86"},
    {"name": "Windows 8.0 Enterprise 64-bit", "value": "Windows_80_Ent_x64"},
    {"name": "Windows 8.0 Enterprise 32-bit", "value": "Windows_80_Ent_x86"},
    {"name": "Windows 7 Enterprise 64-bit", "value": "Windows_7_Ent_x64"},
    {"name": "Windows 7 Enterprise 32-bit", "value": "Windows_7_Ent_x86"},
    {"name": "Windows 10 Professional 64-bit", "value": "Windows_10_Pro_x64"},
    {"name": "Windows 10 Professional 32-bit", "value": "Windows_10_Pro_x86"},
    {"name": "Windows 8.1 Professional 64-bit", "value": "Windows_81_Pro_x64"},
    {"name": "Windows 8.1 Professional 32-bit", "value": "Windows_81_Pro_x86"},
    {"name": "Windows 8.0 Professional 64-bit", "value": "Windows_80_Pro_x64"},
    {"name": "Windows 8.0 Professional 32-bit", "value": "Windows_80_Pro_x86"},
    {"name": "Windows 7 Professional 64-bit", "value": "Windows_7_Pro_x64"},
    {"name": "Windows 7 Professional 32-bit", "value": "Windows_7_Pro_x86"},
    {"name": "Windows Server 2016 Standard 64-bit", "value": "Windows_Server_2016_Std_x64"},
    {"name": "Windows Server 2016 DataCenter 64-bit", "value": "Windows_Server_2016_Dc_x64"},
    {"name": "Windows Server 2012 R2 Standard 64-bit", "value": "Windows_Server_2012_R2_Std_x64"},
    {"name": "Windows Server 2012 Standard 64-bit", "value": "Windows_Server_2012_Std_x64"},
    {"name": "Windows Server 2008 R2 Standard 64-bit", "value": "Windows_Server_2008_R2_Std_x64"},
    {"name": "Windows Server 2008 Standard 64-bit", "value": "Windows_Server_2008_Std_x64"},
    {"name": "Windows Server 2008 Standard 32-bit", "value": "Windows_Server_2008_Std_x86"}
]

os_version_list = [
    {"name": "1511", "value": "1511"},
    {"name": "1607", "value": "1607"}
]

language_list = [
    {"name": "English (US)", "value": "ENU"},
    {"name": "Chinese (Simplified)", "value": "CHS"},
    {"name": "French", "value": "FRA"},
    {"name": "German", "value": "DEU"},
    {"name": "Italian", "value": "ITA"},
    {"name": "Japanese", "value": "JPN"},
    {"name": "German", "value": "KOR"},
    {"name": "Portuguese (Brazil)", "value": "PTB"},
    {"name": "Spanish", "value": "ESP"}
]

vCpu_list = ['1', '2', '3', '4', '5', '6', 'Other']

memory_list = ['256 Mb', '512 Mb', '1024 Mb', '2 Gb', '3 Gb', '4 Gb', '6 Gb', '8 Gb', '12 Gb', '16 Gb', 'Other']

disk_size_list = ['16 Gb','24 Gb','32 Gb','40 Gb','60 Gb','80 Gb','120 Gb','Other']

@ api.route('/')
@ api.route('/home')
def home():
    return 'This is api page.'


@api.route('/GetOSList', methods=['GET', 'POST'])
def get_os_list():
    startTime = datetime.now()
    endTime = datetime.now()
    response = responseDataFormat(True, os_list, None, str(endTime - startTime))
    return RecursiveDumpObject(response)


@api.route('/GetLangList', methods=['GET', 'POST'])
def get_lang_list():
    startTime = datetime.now()
    endTime = datetime.now()
    response = responseDataFormat(True, language_list, None, str(endTime - startTime))
    return RecursiveDumpObject(response)


@api.route('/GetOSVersionList', methods=['GET', 'POST'])
def get_os_version_list():
    startTime = datetime.now()
    endTime = datetime.now()
    response = responseDataFormat(True, os_version_list, None, str(endTime - startTime))
    return RecursiveDumpObject(response)


@api.route('/CreateNewVirtualMachine', methods=['GET', 'POST'])
def create_new_virtual_machine():
    startTime = datetime.now()

    project_name = request.json['project_name']
    guest_os = request.json['guest_os']
    guest_os_version = request.json['guest_os_version']
    language = request.json['language']
    dns_name = request.json['dns_name']
    domain_name = request.json['domain_name']
    vcpu = request.json['vcpu']
    memory = request.json['memory']
    storage = request.json['storage']
    user_name = request.json['user_name']
    password = request.json['password']

    template_name = __get_template_name(guest_os=guest_os, language=language,
                                        guest_os_version=guest_os_version)
    try:
        # Search the new VM DNS name in database
        is_existed = VMList.get_by_name(dns_name)
        if is_existed is not None:
            result = False
            error = "The DNS name of new VM has been existing, please try another one."

        else:
            result = True
            error = ""
            data = []
            name = dns_name
            status = "power off"
            owner = "111"
            uuid = random.randint(100,1000)
            hostname = "Vmhost"
            ip = "10.224.102.13"
            account = user_name
            dnsname = dns_name
            description = "description"

            item = VMList(name, status, owner, uuid, hostname, ip, account, dnsname, description)
            VMList.add_vm_item(item)
            result = True

            response = responseDataFormat(result, data, error, str(endTime - startTime))

        #id = get_task_id()

        #Thread(target=do_new_vm, args=(session['username'],
        #                               project_name,
        #                               template_name,
        #                               dns_name,
        #                               user_name,
        #                               password,
        #                               id)).start()

        #result = True

    except Exception as error:
        result = False
        print error.message

    finally:

        endTime = datetime.now()
        response = responseDataFormat(result, None, error, str(endTime - startTime))

        return RecursiveDumpObject(response)


@api.route('/PowerOn', methods=['GET', 'POST'])
def power_on():
    startTime = datetime.now()
    uuid = request.json['uuid']
    result = False
    message = ""

    try:
        vm = VCenter.get_vm_by_uuid(uuid=uuid)
        vm.power_on_vm()
        result = True
        message = "The virtual machine (" + uuid + ") is powered on."

    except Exception as e:
        print (e.message)

    finally:
        endTime = datetime.now()
        response = responseDataFormat(result, message, None, str(endTime - startTime))
        return RecursiveDumpObject(response)


@api.route('/PowerOff', methods=['GET', 'POST'])
def power_off():
    startTime = datetime.now()
    uuid = request.json['uuid']
    result = False
    message = ""

    try:
        vm = VCenter.get_vm_by_uuid(uuid=uuid)
        vm.power_on_vm()
        result = True
        message = "The virtual machine (" + uuid + ") is powered off."

    except Exception as e:
        print (e.message)

    finally:
        endTime = datetime.now()
        response = responseDataFormat(result, message, None, str(endTime - startTime))
        return RecursiveDumpObject(response)


def __get_template_name(guest_os, language, guest_os_version=None):
    template_name = None

    for os in os_list:
        if os["name"] == guest_os:
            template_name = os["value"]
            break

    for lang in language_list:
        if lang["name"] == language:
            template_name = template_name + "_" + lang["value"]
            break

    if guest_os_version:
        template_name = template_name + "_" + str(guest_os_version)

    return template_name
