from logging import error
from pathlib import Path
import sys
import types
import json

if __name__ != "__main__":
    error("main should not be loaded as a module")
    exit()

def test():
    print("api working")

parsers = {}
def register_parser(name, fn):
    parsers[name] = fn

microservices = []
def add_microservice(microservice):
    microservices.append(microservice)

env = {}
api = {
    "test": test,
    "register_parser": register_parser,
    "add_microservice": add_microservice
}

# https://stackoverflow.com/questions/44956289/how-can-i-exec-a-file-and-provide-hooked-imports-in-python-3
def setup_api_module():
    oscar_api = types.ModuleType('oscar_api')   # create a new module
    oscar_api.__dict__.update(api)              # add the api functions to the module
    sys.modules["oscar_api"] = oscar_api        # add the module to the global list so it can be imported

def main():
    setup_api_module()
    for item in Path("scripts/").glob('*.py'):
        bin = compile(item.read_bytes(), item.name, "exec")
        exec(bin, env)

    sources = sys.argv[1]
    for file in Path(sources).glob("**/*"):
        if file.is_dir(): continue
        for name in parsers:
            parsers[name](file)
    json.dump(microservices, open("microservice_dump.json", "w"))
    json.dump(microservices, open("../../docker/nginx/server/json/microservice_dump.json", "w"))
main()
