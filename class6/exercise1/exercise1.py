#!/usr/bin/env python

from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result

def failed_show_command(task):
    output = task.run(task=networking.netmiko_send_command, command_string="show ip interface brief")

    #if "syntax error" in output.result:
        #print("THIS IS AN INVALID COMMAND")
    if "syntax error" in output.result:
        raise ValueError("THIS IS AN ERROR - INVALID COMMAND")
    
def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(name="srx2")
    #import ipdb; ipdb.set_trace()
    agg_result = nr.run(task=failed_show_command)
    print_result(agg_result)

if __name__=="__main__":
    main()


