#!/usr/bin/env python

from nornir import InitNornir

nr = InitNornir()

def my_first_task(task):
    print(task.host)
    if task.host.data:
        print(task.host.data["dns1"])
        print(task.host["dns2"])
    else:
        print(task.host["dns1"])
        print(task.host["dns2"])   
        
nr.run(task=my_first_task)

