def setup():
    from website.wifi_connect import connect

    # connect to wifi
    if not connect():
        print("Could not connect to internet, abort")
        exit(0)

    # execute setup if necessary
    configs = read_config()
    if configs['setup'] == '0':

        configs['setup'] == 1
        write_configs(configs)
    else:
        print("Packages are already installed")


def write_configs(configs):
    configs = ["=".join([k, v]) for k, v in configs.items()]
    configs=[elem+"\n" for elem in configs]

    with open("config", "w+") as file:
        for l in configs:
            file.write(l)


def read_config():
    with open("config", "r+") as file:
        configs = file.readlines()
        configs = [elem.split("=") for elem in configs]

    configs = {k.strip(): v.strip() for k, v in configs}
    print("Config file :")
    print(configs)
    return configs

