#!/usr/bin/env python

# import general use modules
import os
from pprint import pprint as pp
# import nornir specifics
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.core.task import Result
from nornir.core.filter import F
from nornir.plugins.tasks import networking

def direct(task):
    # Manually create Napalm connection
    #import ipdb; ipdb.set_trace()
    napalm = task.host.get_connection("napalm", task.nornir.config)
    print(napalm)
    print(60 * "#")
    print(napalm.device)
    print(60 * "#")
    print(napalm.device.find_prompt())
    print("END DEVICE OUTPUT")    

    return napalm.device.find_prompt()

def main():
    nr = InitNornir(config_file="config.yaml")
    filt = F(groups__contains="nxos")
    nxos  = nr.filter(filt)
    agg_result = nxos.run(task=direct, num_workers=1)
    print_result(agg_result)

if __name__=="__main__":
    main()

