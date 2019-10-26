#!/usr/bin/env python

# import general use modules
import os
import re
from pprint import pprint as pp
# import nornir specifics
from nornir.plugins.functions.text import print_result
from nornir import InitNornir
from nornir.core.task import Result
from nornir.core.filter import F
from nornir.plugins.tasks import networking

def nxos_checkpoint_1(task):
    # Manually create NAPALM connection
    #import ipdb; ipdb.set_trace()
    task.host.open_connection("napalm", None)
    r = task.host.connections["napalm"].connection._get_checkpoint_file()
    return r

def nxos_checkpoint_2(task):
    napalm_conn = task.host.get_connection("napalm", task.nornir.config)
    checkpoint = napalm_conn._get_checkpoint_file()
    task.host["backup"] = checkpoint
    return checkpoint

def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    filt = F(groups__contains="nxos")
    nxos  = nr.filter(filt)
    #agg_result_1 = nxos.run(task=nxos_checkpoint_1, num_workers=1)
    agg_result_2 = nxos.run(task=nxos_checkpoint_2, num_workers=1)
    #print_result(agg_result_1)
    print_result(agg_result_2)

if __name__=="__main__":
    main()

