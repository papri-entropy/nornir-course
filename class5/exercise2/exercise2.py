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
from nornir.plugins.tasks.networking import netmiko_file_transfer
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.tasks.networking import netmiko_send_config 
from nornir.plugins.tasks.networking import napalm_get

def main():
    
    nr = InitNornir(config_file="config2.yaml", logging={"enabled": False})
    #eos_and_nxos = nr.filter(name="arista1")
    eos_devices = nr.filter(F(groups__contains="eos"))
    #import ipdb; ipdb.set_trace()
    results = eos_devices.run(task=networking.napalm_get, getters=["config"])
    print_result(results)

if __name__=="__main__":
    main()

