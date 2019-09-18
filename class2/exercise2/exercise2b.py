#!/usr/bin/env python

from pprint import pprint as pp
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command

nr = InitNornir(config_file="config.yaml")

nr = nr.filter(platform="ios")

my_results = nr.run(task=netmiko_send_command, command_string="show run | inc hostname")

host_results = my_results['cisco3']

task_result = host_results[0]

#print(my_results)
#print(my_results.items())
#print(host_results)
#for k in host_results:
    #print(k)
print(task_result)
#print(dir(task_result))

#print(task_result.host)
#print(task_result.name)
print(task_result.result)
#print(task_result.failed)

print(type(my_results))
print(type(host_results))
print(type(task_result))
