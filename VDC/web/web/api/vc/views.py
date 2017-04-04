import simplejson as json
import time
from flask import request, session

from web import app
from web.api.core.vcenter import *
from . import vc
from web.tool.jsonHelper import responseDataFormat, RecursiveDumpObject
from datetime import datetime
from web.modules import VMList

import threading


@vc.route('/')
@vc.route('/home')
def home():
    return 'This is api for vCenter.'


@vc.route('/gettaskstatus', methods=['GET','POST'])
def gettaskstatus():
    startTime = datetime.now()
    task_id = request.json['task_id']

    #query task_id
    task = task_list[task_id]
    if (task is None):
        endTime = datetime.now()
        response = responseDataFormat(False, 'Invalid task id', None, str(endTime - startTime))
        return RecursiveDumpObject(response)
  
    endTime = datetime.now()
    response = responseDataFormat(True, task, None, str(endTime - startTime))
    return RecursiveDumpObject(response)


@vc.route('/getalltemplates')
def get_all_templates():
    template_info_list = []
    startTime = datetime.now()
    try:
        vc = GetFreeVCenterConnection()
        template_list = vc.get_all_templates()
        for t in template_list:
            r = dict(t.__dict__)
            del r['_VirtualMachine__snapshot_list']
            del r['_VirtualMachine__vm']
            template_info_list.append(r)
        result = True
    except:
        result = False
    finally:
        FreeVCenterConnection(vc)

        endTime = datetime.now()
        response = responseDataFormat(result, template_info_list, None, str(endTime - startTime))
        return RecursiveDumpObject(response)


@vc.route('/newvm', methods=['GET','POST'])
# proj_name: Project Name
# dns_name: The computer name in guest
# img_name: The template name in vSphere
# size: The scale of guest performance
# user_name: The new user name in guest
# password: The password for new user in guest

def new_vm():
    proj_name = request.json['proj_name']
    template_name = request.json['img_name']
    dns_name = request.json['dns_name']
    user_name= request.json['user_name']
    password = request.json['password']
    #response = responseDataFormat()
    startTime = datetime.now()
    template_name = 'Windows_8.1_Professional_x64_Enu'
    try:
        # Search the new VM DNS name in database
        old_vm = VMList.get_by_name(dns_name)
        if old_vm is not None:
            result = True
            error = "The DNS name of new VM has been existing, please try another one."
            endTime = datetime.now()
            response = responseDataFormat(result, None, error, str(endTime - startTime))
            return  RecursiveDumpObject(response)

        id = GetTaskId();
        threading.Thread(target = do_new_vm, args = (session['username'], proj_name,     template_name,    dns_name,    user_name,    password, id)).start()


        
        result = True

    except Exception as error:
        result = False
        print error.message

    finally:

        endTime = datetime.now()
        response = responseDataFormat(result, id, None, str(endTime - startTime))

        return  RecursiveDumpObject(response)
