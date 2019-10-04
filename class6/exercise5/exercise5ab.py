#!/usr/bin/env python

import os
import logging
import random
from netmiko.ssh_exception import NetMikoAuthenticationException
from nornir.core.exceptions import NornirSubTaskError
from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result

def uptime(task):
    uptime_mapper = {
    "ios": "show clock",
    "eos": "show clock",
    "nxos": "show clock",
    "junos": "show system uptime",
    }
    host = task.host
    platform = host.platform
    cmd = uptime_mapper[platform]

    try:
        task.run(task=networking.netmiko_send_command, command_string=cmd)
    except NornirSubTaskError as e:
        if isinstance(e.result.exception, NetMikoAuthenticationException):
            # Remove the failed task (so ultimately the Nornir print output is cleaner)
            task.results.pop()

            # For failed devices reset the password to the correct value using environment var
            task.host.password = os.environ["NORNIR_PASSWORD"]
        
            # Force Nornir to close stale connections
            try:
                task.host.close_connections()
            except ValueError:
                pass

            task.run(task=networking.netmiko_send_command, command_string=cmd)

        else:
            return f"Unhandled exception: {e}"


def main():
    nr = InitNornir(config_file="config.yaml")

    for host, data in nr.inventory.hosts.items():
        if random.choice([True, False]):
            data.password = "bogus"

    # Printing to understand inventory behavior
    #for x, i in nr.inventory.hosts.items():
        #print(i.password)
    #print(nr.inventory.hosts.items())
    
    # Running Main Task
    agg_result = nr.run(task=uptime, num_workers=1)
    print_result(agg_result)
    
    #import ipdb
    #ipdb.set_trace()
    #for hostname, multi_result in agg_result.items():
        #print()
        #print("-" * 40)
        #print(f"{hostname}: {multi_result[0].result}")
        #print("-" * 40)
        #print()

if __name__=="__main__":
    main()


