from pyVmomi import vim

from config import TemplateConfig
from connection import connect
from tasks import wait_for_tasks


class VirtualMachine:
    __si = connect()

    def __init__(self, vm):

        self.__vm = vm
        if not self.__vm:
            raise SystemExit('Unable to locate virtual machine.')

        self.__snapshot_list = []

        self.uuid = vm.config.uuid
        self.name = vm.name
        self.power_state = vm.runtime.powerState
        self.host_name = vm.runtime.host.name
        self.ip_address = vm.guest.ipAddress

    def get_current_computer_name(self):
        return self.__vm.guest.hostName

    def get_vm_name(self):
        return self.__vm.name

    def reconfig_vm(self, new_name):
        try:
            config = vim.vm.ConfigSpec()
            config.name = new_name
            print dir(self.__vm)
            self.__vm.ReconfigVM_Task(config)


        except Exception as e:
            print e.message

    def add_user_group(self, new_user_name, group_name):
        program_path = 'cmd.exe'
        argument = '/c net localgroup ' + group_name + ' ' + new_user_name + ' /add'

        self.start_program_in_guest(username=TemplateConfig.username,
                                    password=TemplateConfig.password,
                                    program_path=program_path, arguments=argument)

    def create_new_user(self, new_user_name, new_password):
        program_path = 'cmd.exe'
        argument = '/c net user ' + new_user_name + ' ' + new_password + ' /add'

        self.start_program_in_guest(username=TemplateConfig.username,
                                    password=TemplateConfig.password,
                                    program_path=program_path, arguments=argument)

    def change_guest_name(self, new_computer_name):
        old_computer_name = self.get_current_computer_name()
        program_path = 'cmd.exe'
        argument = '/c WMIC ComputerSystem where Name="'+ old_computer_name + '" call Rename Name='+new_computer_name

        self.start_program_in_guest(username=TemplateConfig.username,
                                    password=TemplateConfig.password,
                                    program_path=program_path, arguments=argument)


    def power_on_vm(self):
        try:
            task = [self.__vm.PowerOn()]
            wait_for_tasks(self.__si, tasks=task)

            return 0

        except vim.fault.InvalidPowerState:
            print 'The power state is not poweredOff.'
        except vim.fault.TaskInProgress:
            print 'The virtual machine is busy.'
        except Exception as error:
            return error.message

    def power_off_vm(self):
        try:
            task = [self.__vm.PowerOff()]
            wait_for_tasks(self.__si, tasks=task)

            return  0

        except vim.fault.InvalidPowerState:
            print 'The power state is not poweredOn.'
        except vim.fault.TaskInProgress:
            print 'The virtual machine is busy.'
        except Exception as error:
            return error.message

    def suspend_vm(self):
        try:
            task = [self.__vm.SuspendVM()]
            wait_for_tasks(self.__si, tasks=task)

        except vim.fault.InvalidPowerState:
            print 'The power state is not poweredOn.'

        except vim.fault.TaskInProgress:
            print 'The virtual machine is busy.'

    def reset_vm(self):
        try:
            task = [self.__vm.Reset()]
            wait_for_tasks(self.__si, tasks=task)

        except vim.fault.InvalidPowerState:
            print 'The power state is not suspended.'

        except vim.fault.TaskInProgress:
            print 'The virtual machine is busy.'

    def shutdown_guest(self):
        try:
            task = [self.__vm.ShutdownGuest()]
            wait_for_tasks(self.__si, tasks=task)

        except vim.fault.InvalidPowerState:
            print 'The power state is not poweredOn.'

        except vim.fault.TaskInProgress:
            print 'The virtual machine is busy.'

    def standby_guest(self):
        try:
            task = [self.__vm.StandbyGuest()]
            wait_for_tasks(self.__si, tasks=task)

        except vim.fault.InvalidPowerState:
            print 'The power state is not poweredOn.'

        except vim.fault.TaskInProgress:
            print 'The virtual machine is busy.'

    def reboot_guest(self):
        try:
            task = [self.__vm.RebootGuest()]
            wait_for_tasks(self.__si, tasks=task)

        except vim.fault.InvalidPowerState:
            print 'The power state is not poweredOn.'

        except vim.fault.TaskInProgress:
            print 'The virtual machine is busy.'

        except Exception as error:
            print error.message

    def create_snapshot(self, snapshot_name, description, memory=True, quiesce=False):
        """
        Creates a new snapshot of this virtual machine.
        :param snapshot_name: The name for this snapshot.
        :param description: A description for this snapshot.
        :param memory: If True, a dump of the internal state of the virtual machine is included in the snapshot. Memory
                       snapshots consume time and resources, and thus take longer to create. When set to False, the
                       power state of the snapshot is set to powered off.
        :param quiesce: If True and the virtual machine is powered on when the snapshot is taken, VMware Tools is used
                        to quiesce the file system in the virtual machine. This assures that a disk snapshot represents
                        a consistent state of the guest file system. If the virtual machine is powered off or VMware
                        Tools are not available, the quiesce flag is ignored.
        :return:
        """
        try:
            task = [self.__vm.CreateSnapshot_Task(name=snapshot_name, description=description, memory=memory,
                                                  quiesce=quiesce)]
            wait_for_tasks(self.__si, tasks=task)
        except Exception as error:
            print error.message

    def destroy_vm(self):
        try:
            if self.__vm.runtime.powerState == 'poweredOn':
                self.power_off_vm()

            task = [self.__vm.Destroy_Task()]
            wait_for_tasks(self.__si, tasks=task)
        except Exception as error:
            print error.message

    def revert_snapshot(self, snapshot_name):
        try:
            self.get_snapshot_list()
            for snapshot in self.snapshot_list:
                if snapshot.name == snapshot_name:
                    snapshot_obj = snapshot.snapshot
                    task = [snapshot_obj.RevertToSnapshot_Task()]
                    wait_for_tasks(self.__si, tasks=task)
        except Exception as error:
            print error.message

    def get_snapshot_list(self, listAll, snapshot=None):
        self.__snapshot_list=[] # Clean snapshot list before getting data.
        self.__get_snapshot_list()
        return self.__snapshot_list

    def __get_snapshot_list(self, snapshot=None):
        try:
            if not snapshot:
                ss = self.__vm.snapshot.rootSnapshotList
                if ss:
                    for s in ss:
                        self.__snapshot_list.append(s)
                        self.__get_snapshot_list(s)
            else:
                ss = snapshot.childSnapshotList
                if ss:
                    for s in ss:
                        self.__snapshot_list.append(s)
                        self.__get_snapshot_list(s)
        except AttributeError as error:
            print error.message

    def remove_all_snapshots(self, consolidate=None):
        """
        Remove all the snapshots associated with this virtual machine. If the virtual machine does not have any
        snapshots, then this operation simply return successfully.
        :param consolidate:
        :return:
        """
        try:

            if consolidate:
                task = [self.__vm.RemoveAllSnapshots(consolidate)]
            else:
                task = [self.__vm.RemoveAllSnapshots()]

                wait_for_tasks(self.__si, tasks=task)
        except vim.fault.SnapshotFault:
            print 'There is an error occurs during the snapshot operation.'

    def start_program_in_guest(self, username, password, program_path, arguments=None, working_directory=None,
                               interactive_session=False):
        """
        Starts a program in the guest operating system.
        :param username: The user name in guest.
        :param password: The password in guest
        :param program_path: The absolute path to the program to start.
        :param arguments: The arguments to the program
        :param working_directory: The absolute path of the working directory for the program to be run.
        :param interactive_session: This is set to true if the client wants an interactive session in the guest.
        :return:
        """
        tools_status = self.__vm.guest.toolsStatus
        if tools_status != 'toolsOk':
            raise SystemExit('VMwareTools is either not running or not installed. Rerun the script after verifying that'
                             ' VMwareTools is running.')
        creds = vim.vm.guest.NamePasswordAuthentication()
        creds.username = username
        creds.password = password

        if interactive_session:
            creds.interactiveSession = interactive_session

        try:
            content = self.__si.RetrieveContent()
            pm = content.guestOperationsManager.processManager
            ps = vim.vm.guest.ProcessManager.ProgramSpec()
            ps.programPath = program_path
            if arguments:
                ps.arguments = arguments
            if working_directory:
                ps.workingDirectory = working_directory

            res = pm.StartProgramInGuest(self.__vm, creds, ps)

            if res > 0:
                print 'Program executed, PID is %d' % res

        except Exception as error:
            print error.message
            return -1

        return res

    def list_processes_in_guest(self, username, password, pids=None):
        """
        List the processes running in the guest operating system.
        :param username: The user name in guest.
        :param password: The password in guest
        :param pids: If set, only return information about the specified processes. Otherwise, information about all
                     processes are returned.
        :return:
        """
        tools_status = self.__vm.guest.toolsStatus
        if tools_status != 'toolsOk':
            raise SystemExit(
                'VMwareTools is either not running or not installed. Rerun the script after verifying that'
                ' VMwareTools is running.')

        auth = vim.vm.guest.NamePasswordAuthentication()
        auth.username = username
        auth.password = password

        try:
            content = self.__si.RetrieveContent()
            pm = content.guestOperationsManager.processManager
            if pids is not None:
                res = pm.ListProcessesInGuest(self.__vm, auth, pids)
            else:
                res = pm.ListProcessesInGuest(self.__vm, auth)

        except Exception as error:
            print error.message
            return None

        return res

    def terminate_process_in_guest(self, username, password, pid):
        tools_status = self.__vm.guest.toolsStatus
        if tools_status != 'toolsOk':
            raise SystemExit(
                'VMwareTools is either not running or not installed. Rerun the script after verifying that'
                ' VMwareTools is running.')

        auth = vim.vm.guest.NamePasswordAuthentication()
        auth.username = username
        auth.password = password

        try:
            content = self.__si.RetrieveContent()
            pm = content.guestOperationsManager.processManager
            pm.TerminateProcessInGuest(self.__vm, auth, pid)

        except Exception as error:
            print error.message

    def make_directory_in_guest(self, username, password, directory_path, create_parent_directories=True):
        tools_status = self.__vm.guest.toolsStatus
        if tools_status != 'toolsOk':
            raise SystemExit(
                'VMwareTools is either not running or not installed. Rerun the script after verifying that'
                ' VMwareTools is running.')

        auth = vim.vm.guest.NamePasswordAuthentication()
        auth.username = username
        auth.password = password

        try:
            content = self.__si.RetrieveContent()
            fm = content.guestOperationsManager.fileManager
            fm.MakeDirectoryInGuest(vm=self.__vm, auth=auth, directoryPath=directory_path,
                                    createParentDirectories=create_parent_directories)
        except Exception as error:
            print error.message

    def delete_directory_in_guest(self, username, password, directory_path, recursive=True):
        tools_status = self.__vm.guest.toolsStatus
        if tools_status != 'toolsOk':
            raise SystemExit(
                'VMwareTools is either not running or not installed. Rerun the script after verifying that'
                ' VMwareTools is running.')

        auth = vim.vm.guest.NamePasswordAuthentication()
        auth.username = username
        auth.password = password

        try:
            content = self.__si.RetrieveContent()
            fm = content.guestOperationsManager.fileManager
            fm.DeleteDirectoryInGuest(vm=self.__vm, auth=auth, directoryPath=directory_path, recursive=recursive)
        except Exception as error:
            print error.message

    def delete_file_in_guest(self, username, password, file_path):
        tools_status = self.__vm.guest.toolsStatus
        if tools_status != 'toolsOk':
            raise SystemExit(
                'VMwareTools is either not running or not installed. Rerun the script after verifying that'
                ' VMwareTools is running.')

        auth = vim.vm.guest.NamePasswordAuthentication()
        auth.username = username
        auth.password = password

        try:
            content = self.__si.RetrieveContent()
            fm = content.guestOperationsManager.fileManager
            fm.DeleteFileInGuest(vm=self.__vm, auth=auth, filePath=file_path)
        except Exception as error:
            print error.message
