# Functions to handle documentation of commands registered to the bot
# Stores functions in a dictionary like this:
#
# example_structure = {
#     "module1" : [
#         {"command_name" : 0},
#         {"command_name2" : 0}
#     ],
#     "module2" : [
#         {"command_name3" : 2}
#     ],
#     "module3" : [
#         {"command_name4" : 2}
#     ]
# }

# TODO Truncate/clear all the files before they get appended

mapped_permissions = {
    0 : "Anyone",
    1 : "Followers",
    2 : "Subscribers",
    3 : "Bots",
    4 : "VIPs",
    5 : "Mods",
    6 : "Streamer Only",
}

registered_cmds = {}


def register(cmd_name, module, perm_lvl=0):
    'appends command to a dictionary'

    try:
        registered_cmds[module].append({cmd_name : perm_lvl})
    
    except KeyError:
        registered_cmds.update({module : []})
        registered_cmds[module].append({cmd_name : perm_lvl})
    

def print_cmds_to_file():
    'prints a list of registered chat commands to txt files'

    modules = list(registered_cmds.keys())

    for module in modules:
        for cmd in registered_cmds[module]:
            for name in cmd:
                perm_lvl = cmd[name]
                with open(f"data/cmds/{module}.txt", 'a+',) as f:
                    f.write(f"{name},{perm_lvl}\n")

        print(f"{module}:")
        with open(f"data/cmds/{module}.txt", 'r') as f:
            print(f.read())


def human_readable_permission(lvl):
    return mapped_permissions[lvl]


def print_cmds_to_console():
    'prints a list of registered chat commands to console only'

    modules = list(registered_cmds.keys())

    for module in modules:
        print(f"\n{module}:")
        
        for cmd in registered_cmds[module]:
            for name in cmd:
                perm_lvl = human_readable_permission(cmd[name])
                print(f"!{name} {perm_lvl}")         


# register("test1", "hue", 0)
# register("test", "sfx", 1)
# register("test2", "sfx", 2)
# register("test2", "hue", 3)
print_cmds_to_file()
# print_cmds_to_console()
