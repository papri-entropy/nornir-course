#!/usr/bin/env python
# import general use modules
import os
import re
from pprint import pprint as pp
# import nornir specifics
from nornir import InitNornir
from nornir.core.task import Result
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
from nornir.plugins.tasks import networking
#import ipdb; ipdb.set_trace()

def parse_uptime(uptime_str):
    """
    Extract the uptime string from the given Device.
    Return the uptime in seconds as an integer
    """
    # Initialize to zero        
    (years, weeks, days, hours, minutes, seconds) = (0, 0, 0, 0, 0, 0)
    
    uptime_str = uptime_str.strip()
    time_list = re.split(", | and | uptime is |  ", uptime_str)
    #print(time_list)
    
    for element in time_list:
        if re.search("year", element):
            years = int(element.split()[0])
        elif re.search("week", element):
            weeks = int(element.split()[0])
            #print(weeks)
        elif re.search("day", element):
            days = int(element.split()[0])
            #print(days)
        elif re.search("hour", element):
            hours = int(element.split()[0])
            #print(hours)
        elif re.search("minute", element):
            minutes = int(element.split()[0])
            #print(minutes)
        elif re.search("second", element):
            seconds = int(element.split()[0])
            #print(seconds)
    uptime_sec = (
        (years * 31536000)
        + (weeks * 604800)
        + (days * 86400)
        + (hours * 3600)
        + (minutes * 60)
        + seconds
    )
    return uptime_sec

#print(f"This is just a test to see Juniper not processed by parse_uptime function, the value returned being - " + str(parse_uptime("System booted: 2018-10-03 20:51:06 PDT (48w4d 16:59 ago")))

def uptime_task(task):
    if task.host.groups[0] == "ios" or task.host.groups[0] == "nxos":
        cmd = "show version | inc uptime"
        task.run(task=networking.netmiko_send_command, command_string=cmd)
        print(parse_uptime(task.results.result))
        if parse_uptime(task.results.result) < 86400:
            print(f"{task.host} rebooted recently")
    elif task.host.groups[0] == "eos":
        cmd = "show version | inc Uptime"
        task.run(task=networking.netmiko_send_command, command_string=cmd)
        print(parse_uptime(task.results.result))
        if parse_uptime(task.results.result) < 86400:
            print(f"{task.host} rebooted recently")
    else:
        cmd = "show system uptime | match System"   
        task.run(task=networking.netmiko_send_command, command_string=cmd)
        uptime = 90
        print(uptime)
        if uptime < 86400:
            print(f"{task.host} rebooted recently")
        
    #import ipdb; ipdb.set_trace()
    
    host = task.host
    uptime_str = task.results.result
    print(host, uptime_str)
 
def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    result = nr.run(task=uptime_task)
    print_result(result)

if __name__=="__main__":
    main()

