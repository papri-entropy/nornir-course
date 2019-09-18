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

def vlan_config(task, vlan_id, vlan_name, dry_run=True):
    
    hostname = task.host.name
    #print(hostname)    
    groupname = task.host.groups[0]
    #print(groupname)
    
    commands = f"""vlan {vlan_id} 
        name {vlan_name}"""
    
    # Vlan configuration
    task.run(task=networking.napalm_configure, dry_run=dry_run, configuration=commands)

def main():
    
    VLAN_ID = "1123"
    VLAN_NAME = "cos-vlan1123"
    DRY_RUN = False
    
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    #eos_and_nxos = nr.filter(name="arista1")
    eos_and_nxos = nr.filter(F(groups__contains="eos") | F(groups__contains="nxos"))
    results = eos_and_nxos.run(task=vlan_config, vlan_id=VLAN_ID, vlan_name=VLAN_NAME, dry_run=DRY_RUN, num_workers=1)
    #import ipdb; ipdb.set_trace()
    print_result(results)

if __name__=="__main__":
    main()

