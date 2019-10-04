#!/usr/bin/env python

import os
import logging
from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from getpass import getpass

PASSWORD = getpass()

logger = logging.getLogger("nornir")

def log_show_command(task):
    task.run(task=networking.netmiko_send_command, command_string="show ip interface brief")

def main():
    nr = InitNornir(config_file="config.yaml")
    nr = nr.filter(F(groups__contains="eos"))
    
    # Adding Password To Inventory Data
    for host, data in nr.inventory.hosts.items():
        data.password = PASSWORD
    #import ipdb; ipdb.set_trace()

    # Sending Logging To logging.txt
    logger.info("TESTING INFO LOGGING")
    logger.critical("THIS IS CRITICAL LOGGING STUFF")
    logger.error("THIS IS ERROR LOGGING STUFF")
    logger.debug("THIS IS DEBUG LOGGING STUFF")
    
    # Running Main Task
    agg_result = nr.run(task=log_show_command)
    print_result(agg_result)

if __name__=="__main__":
    main()


