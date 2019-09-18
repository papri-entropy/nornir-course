#!/usr/bin/env python

from nornir import InitNornir

nr = InitNornir()

my_hosts = nr.inventory.hosts

for i in my_hosts:
    print(my_hosts[i].hostname)
    print(my_hosts[i].platform)
    print(my_hosts[i].username)
    print(my_hosts[i].groups[0])
    print(my_hosts[i].password)
    print(my_hosts[i].port)
    print("@@@@@@@@@@@@@@@@@@ NEXT DEVICE @@@@@@@@@@@@@@@@@@")
