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

def vlan_config(task, vlan_id, vlan_name):
    
    hostname = task.host.name
    print(hostname)    
    groupname = task.host.groups[0]
    print(groupname)
    commands = [(f"vlan {vlan_id}"), (f"name {vlan_name}")]
    
    # Netmiko uni test
    uni_test = task.run(
    netmiko_send_command,
    command_string="show vlan",
    use_textfsm=True
    )

    print("-" * 40)
    print(uni_test[0].result)
    print("-" * 40)
    print()
    
    vlan_list = [] 
    for vlan in uni_test[0].result:
        vlan = vlan["vlan_id"]
        vlan_list.append(vlan)
    
    if (f"{vlan_id}") in vlan_list:
        print("VLAN 4 already exists, no changes are necessary!")
    else:
        # Vlan configuration
        results = task.run(task=netmiko_send_config, config_commands=commands)
        print(results[0].result)
            
def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    #eos_and_nxos = nr.filter(name="arista1")
    eos_and_nxos = nr.filter(F(groups__contains="eos") | F(groups__contains="nxos"))
    #eos_and_nxos = eos_and_nxos.inventory.hosts
    #print(eos_and_nxos)

    results = eos_and_nxos.run(task=vlan_config, vlan_id=123, vlan_name="TEST-VLAN123", num_workers=1)
    #print(results)
if __name__=="__main__":
    main()

