#!/usr/bin/env python

import os
from pprint import pprint as pp
from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.tasks.networking import netmiko_send_command

nr = InitNornir(config_file="config.yaml")

ios_filt = F(groups__contains="ios")
eos_filt = F(groups__contains="eos")
nr = nr.filter(ios_filt | eos_filt)

results_arp = nr.run(
    task=napalm_get,
    getters=["arp_table"]
)

#print(results_arp['cisco3'][0].result['arp_table'][0]['ip'])

results_sh_run_static = nr.run(task=netmiko_send_command, command_string="show run | include ip route 0.0.0.0")

#print(results_sh_run_static['cisco3'][0].result.split())

for host in nr.inventory.hosts:
    if "cisco" in host:
        gateway = results_sh_run_static[host][0].result.split()[4]
    else:
        gateway = results_sh_run_static[host][0].result.split()[3]
    for entry in results_arp[host][0].result['arp_table']:
        if gateway == entry['ip']:
            print('Host: ' + host + ', ' + 'Gateway: ' + str(entry)) 
