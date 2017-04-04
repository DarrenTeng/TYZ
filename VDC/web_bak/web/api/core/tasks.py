"""
Helper module for task operations.
"""
from pyVmomi import vmodl
from pyVmomi import vim


def wait_for_tasks(si, tasks):
    """
    Given the service instance si and tasks, it returns after all the tasks are complete.
    """
    property_collector = si.content.propertyCollector

    task_list = [str(task) for task in tasks]

    # Create filter
    obj_specs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task)
                 for task in tasks]
    prop_spec = vmodl.query.PropertyCollector.PropertySpec(type=vim.Task, pathSet=[], all=True)
    filter_spec = vmodl.query.PropertyCollector.FilterSpec()
    filter_spec.objectSet = obj_specs
    filter_spec.propSet = [prop_spec]
    obj_filter = property_collector.CreateFilter(filter_spec, True)

    try:
        version, state = None, None

        # Loop looking for updates till the state moves to a completed state.
        while len(task_list):
            update = property_collector.WaitForUpdates(version)
            for filterSet in update.filterSet:
                for objSet in filterSet.objectSet:
                    task = objSet.obj
                    for change in objSet.changeSet:
                        if change.name == 'info':
                            state = change.val.state
                        elif change.name == 'info.state':
                            state = change.val
                        else:
                            continue

                        if not str(task) in task_list:
                            continue

                        if state == vim.TaskInfo.State.success:
                            # Remove task from taskList
                            task_list.remove(str(task))
                        elif state == vim.TaskInfo.State.error:
                            raise task.info.error
            # Move to next version
            version = update.version
    finally:
        if obj_filter:
            obj_filter.Destroy()
