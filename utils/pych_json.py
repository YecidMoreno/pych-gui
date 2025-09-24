import json

def validate_json(j):
    if not(\
        "plugins" in j and \
        "path" in j["plugins"] and \
        "commIO" in j["plugins"] and \
        "deviceIO" in j["plugins"] and \
        "controlIO" in j["plugins"]\
        ):return False
    
    if not(\
        "commIO" in j\
        ):return False
    
    if not(\
        "deviceIO" in j\
        ):return False
    
    if not(\
        "controlIO" in j\
        ):return False

    return True


def read_json(path):
    with open(path,"r") as f:
        j = json.load(f)
        if validate_json(j):
            return j
    print("JSON no valido")
    return {}

def get_comm_names(j):
    names = []
    names += j["plugins"]["commIO"].keys()
    return names

def get_device_names(j):
    names = []
    names += j["plugins"]["deviceIO"].keys()
    return names

def get_control_names(j):
    names = []
    names += j["plugins"]["controlIO"].keys()
    return names

def get_comm_nodes(j):
    names = []
    names += j["commIO"].keys()
    return names

def get_device_nodes(j):
    names = []
    names += j["deviceIO"].keys()
    return names

def get_control_nodes(j):
    names = []
    names += j["controlIO"].keys()
    return names

def json_details(j):
    print("Plugins loaded")
    print(f" commIO    : {get_comm_names(j)}")
    print(f" deviceIO  : {get_device_names(j)}")
    print(f" controlIO : {get_control_names(j)}")
    print("")
    print("Nodes creaded")
    print(f" commIO    : {get_comm_nodes(j)}")
    print(f" deviceIO  : {get_device_nodes(j)}")
    print(f" controlIO : {get_control_nodes(j)}")