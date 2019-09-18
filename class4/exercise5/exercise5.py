#!/usr/bin/env python
# import general use modules
import os
import re
from pprint import pprint as pp
# import nornir specifics
from nornir import InitNornir
from nornir.core.task import Result
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
from nornir.plugins.tasks import networking
from nornir.plugins.tasks.networking import napalm_get

loopback_123 = """interface Loopback123
   description Hello from NORNIR"""

def main():
    
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    arista4 = nr.filter(name="arista4")
    
    results = arista4.run(task=networking.napalm_get, getters=["config"], retrieve="running")
    arista4_running = results["arista4"].result["config"]["running"]
    #import ipdb; ipdb.set_trace()
    #pp(results["arista4"][0].result)
    #pp(arista4_running)

    conf_l123 = arista4.run(task=networking.napalm_configure, configuration=loopback_123)
    
    conf_replace = arista4.run(task=networking.napalm_configure, configuration=arista4_running, replace=True)

    print_result(conf_l123)
    print_result(conf_replace)

if __name__=="__main__":
    main()

