import oscar_api
import json
import yaml

def parse_yaml(file):
    file_obj = open(file)
    contents = None

    try:
        contents = yaml.safe_load(file_obj)
    except yaml.YAMLError as exc:
        print("error parsing YAML file "+str(file)+": "+str(exc))
    return contents

def parse_json(file):
    file_obj = open(file)
    contents = None

    try:
        contents = json.load(file_obj)
    except json.JSONDecodeError as exc:
        print("error parsing JSON file "+str(file)+": "+str(exc))
    return contents

def parse_asyncapi(file):
    contents = None
    if file.suffix == ".json":
        contents = parse_json(file)
    elif file.suffix == ".yaml":
        contents = parse_yaml(file)

    if type(contents) != dict: return
    if not "asyncapi" in contents.keys(): return

    microservice = {
        "channels": {}
    }

    if "info" in contents:
        if "title" in contents["info"]:
            microservice["name"] = contents["info"]["title"]

    channels = microservice["channels"]
    if not "channels" in contents: return

    for name, channel in contents["channels"].items():
        if not name in channels:
            channels[name] = {
                "publish": False,
                "subscribe": False
            }
        if "publish" in channel:
            channels[name]["publish"] = True
        if "subscribe" in channel:
            channels[name]["subscribe"] = True
    oscar_api.add_microservice(microservice)
    return
    


oscar_api.register_parser("asyncapi", parse_asyncapi)