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
from nornir.plugins.tasks import files

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


def write_checkpoint(task):
    backup_path = f"/home/petrache/nornir-course/class7/exercise5/backups/"
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)
    filename = f"{backup_path}{task.host.name}_checkpoint"
    content = task.host["backup"]
    result = task.run(task=files.write_file, filename=filename, content=content)
    return result    

def main():
    nr = InitNornir(config_file="config.yaml", logging={"enabled": False})
    filt = F(groups__contains="nxos")
    nxos  = nr.filter(filt)
    
    checkpoint_1_option = nxos.run(task=nxos_checkpoint_1, num_workers=1)
    checkpoint_2_option = nxos.run(task=nxos_checkpoint_2, num_workers=1)
    
    #print_result(checkpoint_1_option)
    print_result(checkpoint_2_option)

    write_backup = nxos.run(task=write_checkpoint, num_workers=1)

if __name__=="__main__":
    main()

