#!/usr/bin/env python

# import general use modules
import os
from pprint import pprint as pp
# import nornir specifics
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.core.filter import F

def main():
    nr = InitNornir(config_file="config.yaml")
    
    hosts = nr.inventory.hosts
    #print(hosts)

    eos_group = nr.filter(F(groups__contains="eos"))
    eos_hosts = eos_group.inventory.hosts
    #print(eos_hosts)

    int_status = eos_group.run(task=netmiko_send_command, command_string="show interface status", use_textfsm=True)
    #print(int_status['arista4'][0].result)

    d = {}
    for arista in eos_hosts:
        #print(arista)
        d[arista] = {}
        for element in int_status[arista][0].result:
            interface = element['port']
            print(interface)
            status = element['status']
            print(status)
            vlan = element['vlan']
            print(vlan)

            d[arista][interface] = {}
            d[arista][interface]['status'] = status
            d[arista][interface]['vlan'] = vlan
    pp(d)           

if __name__=="__main__":
    main()
