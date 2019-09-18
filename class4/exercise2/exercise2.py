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
from nornir.plugins.tasks.networking import netmiko_file_transfer
from nornir.plugins.tasks.networking import netmiko_send_command

def scp_copy(task):
    # Obtain the platform name    
    platform = task.host.platform
    # Set the filename based on the platform and inventory data
    base_file = task.host["file_name"]
    source_file = f"{platform}/{base_file}"
    dest_file = base_file

    # Transfer the file
    results = task.run(
    netmiko_file_transfer,
    source_file=source_file,
    dest_file=dest_file,
    overwrite_file=True,
    direction="put"
    )

    # Netmiko uni test
    uni_test = task.run(
    netmiko_send_command,
    command_string="more flash:/arista_test.txt",
    use_textfsm=True
    )

    

    print()
    print("-" * 40)
    print(task.host)
    print(source_file)
    print()
    if results[0].changed is False:
        print("File not transferred: correct file is already on the device")
    else:
        print("File transferred")
    if results[0].result is True:
        print("Remote file exists and is correct")
    print("-" * 40)
    print(uni_test[0].result)
    print("-" * 40)
    print()

def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    #eos= nr.filter(name="arista1")
    eos = nr.filter(F(groups__contains="eos"))
    results = eos.run(task=scp_copy, num_workers=1)

if __name__=="__main__":
    main()

