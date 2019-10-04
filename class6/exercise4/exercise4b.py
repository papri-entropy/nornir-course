#!/usr/bin/env python

import os
import logging
from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result

def session_log_show_command(task):
    #import ipdb; ipdb.set_trace()
    
    # Dynamically set the session log to be unique per host
    session_log_filename = f"{task.host}-session-log.txt"
    group_object = task.host.groups.refs[0]
    group_object.connection_options["netmiko"].extras["session_log"] = session_log_filename

    # Running Custom Task Using Netmiko     
    task.run(task=networking.netmiko_send_command, command_string="show run | i hostname")

def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
   
    # Set password using env var
    for host, host_obj in nr.inventory.hosts.items():
        #print(host, host_obj.password)
        host_obj.password = os.environ["NORNIR_PASSWORD"]
        #print(host, host_obj.password)
 
    # Running Main Task
    agg_result = nr.run(task=session_log_show_command, num_workers=1)
    #import ipdb
    #ipdb.set_trace()
    print_result(agg_result)

if __name__=="__main__":
    main()


