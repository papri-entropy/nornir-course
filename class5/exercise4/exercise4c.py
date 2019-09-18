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
from nornir.plugins.tasks import text

def jinja_template(task):
    
    yaml_load = task.run(task=data.load_yaml, file=f"/home/petrache/nornir-course/class5/junos/{task.host.name}.yaml")
 
    for rule in yaml_load[0].result["my_acl"]:
        if rule["term_name"] == "rule1":
            r1 = rule["term_name"]
            r1_protocol = rule["protocol"]
            r1_dest_port = rule["destination_port"]
            r1_dest_addr = rule["destination_address"]
            r1_state = rule["state"]
            #print(r1_protocol,r1_dest_port,r1_dest_addr,r1_state)
    
 
        if rule["term_name"] == "rule2":
            r2 = rule["term_name"]
            r2_protocol = rule["protocol"]
            r2_dest_port = rule["destination_port"]
            r2_dest_addr = rule["destination_address"]
            r2_state = rule["state"]
            #print(r2_protocol,r2_dest_port,r2_dest_addr,r2_state)

        if rule["term_name"] == "rule3":
            r3 = rule["term_name"]
            r3_protocol = rule["protocol"]
            r3_dest_port = rule["destination_port"]
            r3_dest_addr = rule["destination_address"]
            r3_state = rule["state"]
            #print(r3_protocol,r3_dest_port,r3_dest_addr,r3_state)

    multi_result = task.run(task=text.template_file, template="acl.j2", path="/home/petrache/nornir-course/class5/templates/junos/", r1=r1, r1_protocol=r1_protocol, r1_dest_port=r1_dest_port, r1_dest_addr=r1_dest_addr, r1_state=r1_state, r2=r2, r2_protocol=r2_protocol, r2_dest_port=r2_dest_port, r2_dest_addr=r2_dest_addr, r2_state=r2_state, r3=r3, r3_protocol=r3_protocol, r3_dest_port=r3_dest_port, r3_dest_addr=r3_dest_addr, r3_state=r3_state)    

    rendered_acl = multi_result[0].result
    #print(rendered_acl)
    task.host["rendered_acl"] = rendered_acl
    #print(task.host.data["rendered_acl"])
    
def main():
    
    nr = InitNornir(config_file="config4.yaml", logging={"enabled": False})
    srx2 = nr.filter(name="srx2")
    #import ipdb; ipdb.set_trace()
    results = srx2.run(task=jinja_template)
    print(results["srx2"][2].result)

if __name__=="__main__":
    main()

