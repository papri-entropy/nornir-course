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
        result =  "VLAN 4 already exists, no changes are necessary!"
        changed = False
        failed = False
        return Result(host=task.host, result=result, changed=changed, failed=failed)
    
    changed = True
    # Vlan configuration
    multi_result = task.run(task=netmiko_send_config, config_commands=commands)
    
    if (
        "%Invalid command" in multi_result[0].result
        or "% Invalid input" in multi_result[0].result
    ):
        failed = True
        result_msg = "An invalid configuration command was used."
    else:
        # Note task still could be marked at failed from the "netmiko_send_config"
        # execution i.e. at the MultiResult level.
        failed = False
        result_msg = f"Configured vlan {vlan_id} with name {vlan_name}!"

    return Result(host=task.host, result=result_msg, changed=changed, failed=failed)


def main():
    
    VLAN_ID = "1001"
    VLAN_NAME = "cos-vlan"
    
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    #eos_and_nxos = nr.filter(name="arista1")
    #import ipdb; ipdb.set_trace()
    eos_and_nxos = nr.filter(F(groups__contains="eos") | F(groups__contains="nxos"))
    results = eos_and_nxos.run(task=vlan_config, vlan_id=VLAN_ID, vlan_name=VLAN_NAME, num_workers=1)
    print_result(results)

if __name__=="__main__":
    main()

