from logging import error
from pathlib import Path
import sys
import types

if __name__ != "__main__":
    error("main should not be loaded as a module")
    exit()

def test():
    print("api working")

parsers = {}
def register_parser(name, fn):
    parsers[name] = fn

env = {}
api = {
    "test": test,
    "register_parser": register_parser
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

    for name in parsers:
        parsers[name]()
main()
