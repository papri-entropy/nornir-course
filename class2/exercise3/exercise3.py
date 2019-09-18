#!/usr/bin/env python

import os
from pprint import pprint as pp
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result


nr = InitNornir(config_file="config.yaml")

ios_filt = F(groups__contains="ios")
eos_filt = F(groups__contains="eos")
nr = nr.filter(ios_filt | eos_filt)

results_arp = nr.run(task=netmiko_send_command, command_string="show ip arp")
#print(results_arp['cisco3'][0].result.splitlines())

results_sh_run_static = nr.run(task=netmiko_send_command, command_string="show run | include ip route 0.0.0.0")
#print(results_sh_run_static['cisco3'][0].result.split())

for host in nr.inventory.hosts:
    if "cisco" in host:
        gateway = results_sh_run_static[host][0].result.split()[4]
    else:
        gateway = results_sh_run_static[host][0].result.split()[3]

    for line in results_arp[host][0].result.splitlines():
        if gateway in line:
            gw_arp_entry = line.strip()
    print('Host: ' + host + ', ' + 'Gateway: ' + gw_arp_entry) 
