"""
Routes and views for the flask application.
"""
import simplejson as json
from datetime import datetime
from flask import render_template, redirect, request, url_for, session, escape, jsonify, make_response
from web import app, db
#from web.utils.control_vm import *
from modules import Users
from modules import VMList
from web.tool.jsonHelper import RecursiveDumpObject, RecursiveEncoder, responseDataFormat
import time

@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    """Renders the home page."""
    if 'username' in session:
        return  redirect('../static/Home.html')
    else:
        return redirect(url_for('user.login'))

@app.route('/vm_list_all', methods=['GET', 'POST'])
def VMListAll():
    VMs = VMList.get_vm_all()
    #print r = dict(VMs__dict__)
    #json.dumps(VMs)
    for vm in VMs:
        print vm.name
    return render_template('vdc_list.html',VMs = VMs)

@app.route('/newVMItem', methods=['GET', 'POST'])
def newVMItem():
    data = []
    duration = 0
    result = True
    error = ""
    startTime = datetime.now()
    if request.method == 'POST':
        name = "VM2"
        status = "power off"
        owner = "111"
        uuid = "12345678"
        hostname = "Vmhost"
        ip = "10.224.102.13"
        account = "user1"
        dnsname = "test"
        description = "description"

        vmitem = VMList(name,status,owner,uuid,hostname,ip,account,dnsname,description)
        VMList.add_vm_item(vmitem)
        endTime = datetime.now()
        duration = endTime - startTime
        response = responseDataFormat(result,data,error,str(duration))
        return RecursiveDumpObject(response);
@app.route('/moveTo', methods=['GET', 'POST'])
def moveVMItem():
    data = []
    duration = 0
    result = True
    error = ""
    startTime = datetime.now()
    try:
        if request.method == 'POST':
            uuid = request.json['uuid']
            owner = request.json['owner']
            user = Users.get_by_username(owner)
            if(user != None):
                if(VMList.update_vm_byname(uuid,owner)):
                    endTime = datetime.now()
                    duration = endTime - startTime
                    response = responseDataFormat(result,data,error,str(duration))
                    return RecursiveDumpObject(response);
                else:
                    result = False
                    error = "Update Failed!"  
            else:
                result = False
                error = "User not exist!"
    except Exception as error:
            result = False
            print error.message
    finally:
            endTime = datetime.now()
            response = responseDataFormat(result, None, error, str(endTime - startTime))

            return  RecursiveDumpObject(response)

@app.route('/delVMItem', methods=['GET', 'POST'])
def delVMItem():
    data = []
    duration = 0
    result = True
    error = ""
    startTime = datetime.now()
    if request.method == 'POST':
        uuid = request.json['uuid']
        if(VMList.delete_vm_byname(uuid)):
            endTime = datetime.now()
            duration = endTime - startTime
            response = responseDataFormat(result,data,error,str(duration))
            return RecursiveDumpObject(response);
        else:
            endTime = datetime.now()
            duration = endTime - startTime
            result = False
            response = responseDataFormat(result,data,error,str(duration))
            return RecursiveDumpObject(response);

@app.route('/GetVMList', methods=['GET', 'POST'])
def GetVMList():
    #data = []
    duration = 0
    result = True
    error = ""
    startTime = datetime.now()
    if 'username' in session:
        owner = escape(session['username'])
        VMs = VMList.get_by_owner(owner)
        data = [r.as_dict() for r in VMs]
        #data = jsonify(result=result)
        #for r in VMs:  
            #jsonVM = dict(r.items())
            #jsonVM = {}   
            #jsonVM['name'] = r.name 
            #jsonVM['status'] = r.status  
            #jsonVM['owner'] = r.owner 
            #jsonVM['uuid'] = r.uuid  
            #jsonVM['hostname'] = r.hostname  
            #jsonVM['ip'] = r.ip 
            #jsonVM['account'] = r.account 
            #data.append(jsonVM)  
        endTime = datetime.now()
        duration = endTime - startTime
        response = responseDataFormat(result,data,error,str(duration))
        return RecursiveDumpObject(response);
    else:
        result = False
        error = "User not exist!"
        return RecursiveDumpObject(response);

@app.route('/getCurrentUser')
def getCurrentUser():
    data = {}
    duration = 0
    result = True
    error = ""
    if 'username' in session:
        data['name'] = escape(session['username'])
        response = responseDataFormat(result,data,error,duration)
        return RecursiveDumpObject(response);
    else:
        result = False
        error = "User not exist!"
        return RecursiveDumpObject(response);

@app.route('/Create', methods=['GET', 'POST'])
def Create():
    data = request.json['uuid']
    CloneVm(data, 'newVM')
    return "success"

@app.route('/PowerOff', methods=['GET', 'POST'])
def PoewerOff():
    data = request.json['uuid']
    PowerOffVm(data)
    return "success"

@app.route('/PowerOn', methods=['GET', 'POST'])
def PoewerOn():
    data = request.json['uuid']
    PowerOnVm(data)
    return "success"



@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/newVM', methods=['GET', 'POST'])
def newVM():
    if request.method == 'POST':
        VMName = request.form['VM_NAME']
        VMTemp = request.form['VM_TEMPLATE']
        VMSize = request.form['VM_SIZE']
        VMUserName = request.form['VM_USER_NAME']
        VMPassword = request.form['VM_PASSWORD']
        VMConfirmPassword = request.form['VM_CONFIRM_PASSWORD']

        error='None'

        return render_template("new_VM.html", error=error)
    else:
        VMTempList = ['Windows XP', 'Windows 7', 'windows 8']
        VMSizeList = ['100', '200', '300']
        return render_template("new_VM.html", VMTempList=VMTempList, VMSizeList=VMSizeList)

@app.route('/test1')
def test1():
	return render_template("test1.html")

@app.route('/GetRDP', methods=['GET'])
def GetRDP():
    IP = request.args.get('IP')
    data = 'full address:s:' + IP
    response = make_response(data)
    response.mimetype="application/rdp"
    response.headers["Content-Disposition"] = "attachment; filename=" + IP + ".rdp"
    return response