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
from nornir.plugins.tasks import data

def firewall_rules(task):
   
    yaml_load = task.run(task=data.load_yaml, file=f"/home/petrache/nornir-course/class5/junos/{task.host.name}.yaml")
    
    #pp(yaml_load[0].result)
    #pp(yaml_load[0].result["my_acl"][0]["destination_address"])
    
    for rule in yaml_load[0].result["my_acl"]:
        if rule["term_name"] == "rule1":
            r1 = rule["term_name"]
            r1_protocol = rule["protocol"]
            r1_dest_port = rule["destination_port"]
            r1_dest_addr = rule["destination_address"]
            r1_state = rule["state"]
            print(r1_protocol,r1_dest_port,r1_dest_addr,r1_state)
    
 
        if rule["term_name"] == "rule2":
            r2 = rule["term_name"]
            r2_protocol = rule["protocol"]
            r2_dest_port = rule["destination_port"]
            r2_dest_addr = rule["destination_address"]
            r2_state = rule["state"]
            print(r2_protocol,r2_dest_port,r2_dest_addr,r2_state)

        if rule["term_name"] == "rule3":
            r3 = rule["term_name"]
            r3_protocol = rule["protocol"]
            r3_dest_port = rule["destination_port"]
            r3_dest_addr = rule["destination_address"]
            r3_state = rule["state"]
            print(r3_protocol,r3_dest_port,r3_dest_addr,r3_state)
    

    fw_rules = f"""
    set firewall family inet filter my_acl term {r1} from protocol {r1_protocol}
    set firewall family inet filter my_acl term {r1} from destination-port {r1_dest_port}
    set firewall family inet filter my_acl term {r1} from destination-address {r1_dest_addr}
    set firewall family inet filter my_acl term {r1} then {r1_state}
    set firewall family inet filter my_acl term {r2} from protocol {r2_protocol}
    set firewall family inet filter my_acl term {r2} from destination-port {r2_dest_port}
    set firewall family inet filter my_acl term {r2} from destination-address {r2_dest_addr}
    set firewall family inet filter my_acl term {r2} then {r2_state}
    set firewall family inet filter my_acl term {r3} from protocol {r3_protocol}
    set firewall family inet filter my_acl term {r3} from destination-port {r3_dest_port}
    set firewall family inet filter my_acl term {r3} from destination-address {r3_dest_addr}
    set firewall family inet filter my_acl term {r3} then {r3_state}
    """

    print(fw_rules)

def main():
    
    nr = InitNornir(config_file="config3.yaml", logging={"enabled": False})
    srx2 = nr.filter(name="srx2")
    #import ipdb; ipdb.set_trace()
    results = srx2.run(task=firewall_rules)
    #print_result(results)

if __name__=="__main__":
    main()

