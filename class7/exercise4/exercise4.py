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
    # Set the filename based on the platform and inventory data
    source_file = "scp_copy_example.txt"
    dest_file = source_file

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
    command_string="dir bootflash:/scp_copy_example.txt",
    use_textfsm=True
    )

    print()
    print("-" * 40)
    print(task.host)
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

def netmiko_prompting_del(task):
    """ 
    Some commands prompt for confirmation:

    nxos1# del bootflash:/text.txt
    Do you want to delete "/text.txt" ? (yes/no/abort)   [y] y
    """

    # Manually create Netmiko connection

    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    
    filename = "scp_copy_example.txt"
    del_cmd = f"del bootflash:/{filename}"

    cmd_list = [del_cmd, "\n"]
    output = ""

    import ipdb
    ipdb.set_trace()
    
    for cmd in cmd_list:
        # Use timing mode
        output += net_connect.send_command_timing(
            cmd, strip_prompt=False, strip_command=False
        )

    print()
    print("#" * 80)
    print(task.host.name)
    print("---")
    print(output)
    print("#" * 80)
    print()

def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    nxos1= nr.filter(name="nxos1")
    scp_job = nxos1.run(task=scp_copy, num_workers=1)
    delete_job = nxos1.run(task=netmiko_prompting_del, num_workers=1)

if __name__=="__main__":
    main()

