import oscar_api

print("initialising script1")
# print(dir())

var1 = "variable 1"

oscar_api.test()

def set_var():
    global var1
    var1 = 5

oscar_api.register_parser("v1", lambda: print(var1))
oscar_api.register_parser("v2", set_var)
oscar_api.register_parser("v3", lambda: print(var1))