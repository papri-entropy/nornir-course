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

def snmp_id(task):
    
    hostname = task.host.name
    groupname = task.host.groups[0]
    #print(task.host)
    #print(task.host.name)
    #print(task.host.hostname)
    #print(groupname)
    #print(task.host["snmp_id"])
    
    if task.host.groups[0] == "ios":
        ios_snmp_id = task.host.data["snmp_id"]
        cmd = f"snmp-server chassis-id {ios_snmp_id}"
        print(cmd)
        multi_result = task.run(task=networking.netmiko_send_config, config_commands=cmd)
    elif task.host.groups[0] == "eos":
        eos_snmp_id = task.host["snmp_id"]
        cmd = f"snmp chassis-id {eos_snmp_id}-{task.host.name}"
        print(cmd)
        multi_result = task.run(task=networking.netmiko_send_config, config_commands=cmd)


def main():
    
    nr = InitNornir(config_file="config1.yaml", logging={"enabled": False})
    #eos_and_nxos = nr.filter(name="arista1")
    #import ipdb; ipdb.set_trace()
    ios_and_eos = nr.filter(F(groups__contains="ios") | F(groups__contains="eos"))
    results = ios_and_eos.run(task=snmp_id, num_workers=1)
    print_result(results)

if __name__=="__main__":
    main()

