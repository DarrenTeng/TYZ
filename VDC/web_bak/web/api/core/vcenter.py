from pyVmomi import vim
import time
from connection import connect
from virtualmachine import VirtualMachine
from tasks import wait_for_tasks
import uuid
import threading
from flask import request, session
from web.modules import VMList

VCenterList = [];

task_list = {}
g_task_id = 0

def get_task_id():
    global g_task_id 
    g_task_id += 1
    return g_task_id

g_vm_cache = {}

def GetVMFromTemplateCache(template_name):
    vc = GetFreeVCenterConnection()
    uuid = r'4208eea1-c7fd-53ba-da74-33d23ae489a7'
    #vm = vc.get_vm_by_name('test1234')
    vm = vc.get_vm_by_uuid(uuid=uuid)
    FreeVCenterConnection(vc)
    return vm

    global g_vm_cache
    try:
        template_cache = g_vm_cache[template_name]
    except:
        template_cache = []
    if (len(template_cache) == 0):
        #threading.Thread(target=CreateCache, args=(template_name)).start()
        vm = CreateVM(template_name)
        return vm
   
    vm = template_cache.pop()
    threading.Thread(target=CreateVM, args=(template_name)).start()
    return vm

def CreateCache(template_name):
    global g_vm_cache
    template_cache = []
    vc = GetFreeVCenterConnection()
    for i in range(1):
        vm = CreateVM(template_name)
        template_cache.append(vm)
    FreeVCenterConnection(vc)

    g_vm_cache[template_name] = template_cache

def CreateVM(template_name):
    vc = GetFreeVCenterConnection()
    name = template_name + str(uuid.uuid1())       
    vc.clone_vm_from_template(template_name=template_name, vm_name= name, folder_name='Template_Caches')
    vm = vc.get_vm_by_name(name)
        
    FreeVCenterConnection(vc)

    return vm


def do_new_vm(owner_name, proj_name,     template_name,    dns_name,    user_name,    password, id):
    try:
        task_list[id] = 'Running'

        vc = GetFreeVCenterConnection()
       
        vm = GetVMFromTemplateCache(template_name)
        vm.reconfig_vm(dns_name)

        #vc.clone_vm_from_template(template_name=template_name, vm_name=dns_name,folder_name=proj_name)
        
        #vm = vc.get_vm_by_name(dns_name)
        #vm.create_snapshot('clear', 'clear')

        vm.power_on_vm()
        time.sleep(30)
        vm = vc.get_vm_by_name(dns_name)
        vm.create_new_user(user_name, password)
        time.sleep(5)
        vm.add_user_group(user_name, 'Administrators')

        

        # Add new virtual machine to database.
        name = vm.name
        status = vm.power_state
        owner = owner_name
        uuid = vm.uuid
        hostname = vm.host_name
        ip = vm.ip_address
        account = user_name
        dnsname = dns_name
        description = ""

        vm_item = VMList(name=name, status=status, owner=owner, uuid=uuid, hostname=hostname, ip=ip, account=account, dnsname = dnsname, description = description)
        VMList.add_vm_item(vm_item)
        task_list[id] = 'Done'

        result = True

    except Exception as error:
        result = False
        print error.message
        task_list[id] = 'Error' + error.message


    finally:
        FreeVCenterConnection(vc)

      
        return

all_templates = []

def GetFreeVCenterConnection():
    si = None
    if (len(VCenterList) != 0):
        si = VCenterList.pop()
        si.isBusy = True
    else:
        si = VCenter()

    return si

def FreeVCenterConnection(si):
    si.isBusy = False
    VCenterList.append(si)


class VCenter(object):
    def __init__(self):
        self.__si = connect()
        self.isBusy = False

    def get_vm_by_uuid(self, uuid):
        vm = VirtualMachine(self.__get_obj_by_uuid(uuid))
        return vm

    def get_vm_by_name(self, name):
        vim_type = [vim.VirtualMachine]
        objects = self.__get_all_objects_by_type(vim_type)
        all_vms = []

        for obj in objects:
            try:
                if not obj.config.template:
                    all_vms.append(VirtualMachine(obj))
            except:
                pass

        for vm in all_vms:
            if vm.name == name:
                return vm

        return -1

    def __get_obj_by_uuid(self, uuid):

        obj = self.__si.content.searchIndex.FindByUuid(None, uuid, True)
        if not obj:
            print('Unable to find to object with supplied info')
            return None
        return obj

    def __get_obj_by_name(self, name):

        target_obj = None
        objects = self.get_all_objects_by_type()

        for obj in objects:
            if obj.name == name:
                target_obj = obj
                break

        return target_obj

    def get_all_vms(self):
        all_vms = []

        vim_type = [vim.VirtualMachine]
        objects = self.__get_all_objects_by_type(vim_type)
        for obj in objects:
            if not obj.config.template:
                all_vms.append(VirtualMachine(obj))

        return all_vms

    def get_all_templates(self):
        global all_templates
        if (len(all_templates) != 0):
            return all_templates
        vim_type = [vim.VirtualMachine]
        objects = self.__get_all_objects_by_type(vim_type)
        for obj in objects:
            try:
                if obj.config.template:
                    all_templates.append(VirtualMachine(obj))
            except:
                pass

        return all_templates

    def __get_all_templates(self):
        all_templates = []
        vim_type = [vim.VirtualMachine]
        objects = self.__get_all_objects_by_type(vim_type)
        for obj in objects:
            try:
                if obj.config.template:
                    all_templates.append(obj)
            except:
                pass # If a virtual machine is cloning, the template property is null, add a except here to catch this exception.

        return all_templates



    def __get_all_objects_by_type(self, vim_type=None):
        # Need to update after demo, this method is only find virtual machine, folder, template in Test Datacenter.
        objects = []

        content = self.__si.RetrieveContent()
        container = content.rootFolder
        dc = None
        view_type = [vim.Datacenter]
        recursive = True
        container_dc_view = content.viewManager.CreateContainerView(container,
                                                                 view_type,
                                                                 recursive)
        for obj in container_dc_view.view:
            if obj.name == 'Test Datacenter':
                dc = obj

        if vim_type:
            view_type = vim_type
        else:
            view_type = []

        if vim_type == [vim.VirtualMachine]:
            container_dc = dc.hostFolder
            container_view = content.viewManager.CreateContainerView(container_dc,
                                                                     view_type,
                                                                     recursive)
            for obj in container_view.view:
                objects.append(obj)

        elif vim_type == [vim.Folder]:
            if not dc:
                raise SystemError('Unable to get Test Datacenter with supplied info.')

            for obj in dc.vmFolder.childEntity:
                if type(obj)==view_type[0]:
                    objects.append(obj)

        else:
            container_view = content.viewManager.CreateContainerView(container,
                                                                     view_type,
                                                                     recursive)

            for obj in container_view.view:
                objects.append(obj)

        return objects

    def clone_vm_from_template(self, template_name, vm_name, folder_name=None, host_name=None, ds_name=None, rp_name=None):
        if folder_name == None:
            folder_name = 'Test'

        if host_name == None:
            host_name = '10.224.104.31'

        if ds_name == None:
            ds_name = 'local2-2'

        template = None
        templates = self.__get_all_templates()
        for t in templates:
            if t.name == template_name:
                template = t
                break

        if not template:
            raise SystemError('Unable to get template with supplied info.')

        folder = None
        folders = self.__get_all_objects_by_type(vim_type=[vim.Folder])


        for f in folders:
            if f.name == folder_name:
                folder = f
                break

        if not folder:
            raise SystemError('Unable to get folder with supplied info.')

        resource_pool = None
        resource_pools = self.__get_all_objects_by_type(vim_type=[vim.ResourcePool])
        if rp_name:
            for rp in resource_pools:
                if rp.name == rp_name:
                    resource_pool = rp
                    break
        else:
            for rp in resource_pools:
                if rp.owner.name == host_name and rp.name == 'Resources':
                    resource_pool = rp
                    break

        if not resource_pool:
            raise SystemError('Unable to get resource pool with supplied info.')

        datastore = None
        datastores = self.__get_all_objects_by_type(vim_type=[vim.Datastore])
        for ds in datastores:
            if ds.name == ds_name:
                datastore = ds
                break

        if not datastore:
            raise SystemError('Unable to get to datastore with supplied info.')

        relocate_spec = vim.vm.RelocateSpec()
        relocate_spec.datastore = datastore
        relocate_spec.pool = resource_pool

        clone_spec = vim.vm.CloneSpec()
        clone_spec.location = relocate_spec
        clone_spec.powerOn = False

        task = [template.Clone(folder=folder, name=vm_name, spec=clone_spec)]
        #task = [template.cl]
        wait_for_tasks(self.__si,task)



if __name__=='__main__':
    pass
