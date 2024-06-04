from dpdispatcher import Machine, Resources

def get_machine_and_resources(machine: str, resources: str) -> tuple[Machine, Resources]:
    '''
    Used to get machine and resources from json file or dpdispatcher.Machine

    Args:
        machine (str): machine information in json file or dpdispatcher.Machine
        resources (str): resources information in json file or dpdispatcher.Machine
    '''
    my_machine = None
    my_resources = None

    if isinstance(machine, str):
        my_machine = Machine.load_from_json(machine)
    elif isinstance(machine, Machine):
        my_machine = machine
    else:
        raise TypeError('machine should be str or dpdispatcher.Machine')
    
    if isinstance(resources, str):
        my_resources = Resources.load_from_json(resources)
    elif isinstance(resources, Resources):
        my_resources = resources
    else:
        raise TypeError('resources should be str or dpdispatcher.Resources')
    
    return my_machine, my_resources