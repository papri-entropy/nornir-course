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

output = nr.run(task=netmiko_send_command, command_string="show ip interface brief")

print_result(output)
