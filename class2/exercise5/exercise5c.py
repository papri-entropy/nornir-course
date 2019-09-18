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

nr = nr.filter(ios_filt)

nr.inventory.hosts["cisco3"].password = 'bogus'

output1 = nr.run(task=netmiko_send_command, command_string="show ip interface brief")

print_result(output1)

print(output1.failed_hosts)

print(nr.data.failed_hosts)

try:
    # Remove "cisco3" from the Nornir connection table
    nr.inventory.hosts["cisco3"].close_connections()
except ValueError:
    pass

if nr.data.failed_hosts:
    nr.inventory.hosts["cisco3"].password = os.environ["NORNIR_PASSWORD"]
    output2 = nr.run(task=netmiko_send_command, command_string="show ip int brief", on_good=False, on_failed=True)
    print_result(output2)


