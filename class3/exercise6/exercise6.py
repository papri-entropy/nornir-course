#!/usr/bin/env python

# import general use modules
import os
from pprint import pprint as pp
# import nornir specifics
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
from nornir.plugins.tasks.networking import napalm_get

def main():
    nr = InitNornir(config_file="config.yaml")
    
    nxos_group = nr.filter(F(groups__contains="nxos"))
    nxos_hosts = nxos_group.inventory.hosts
    #print(nxos_hosts)

    results = nxos_group.run(task=napalm_get, getters=['config', 'facts'], getters_options={'config': {'retrieve': 'all'}})
    #print_result(results)

    d = {}
    for nxos in nxos_hosts:
        d[nxos] = {}
        
        model = results[nxos][0].result['facts']['model']
        #pp(model)
        uptime = results[nxos][0].result['facts']['uptime']
        #pp(uptime)
        vendor = results[nxos][0].result['facts']['vendor']
        #pp(vendor)
        running = results[nxos][0].result['config']['running'].splitlines()[5:]
        startup = results[nxos][0].result['config']['startup'].splitlines()[5:]
        #pp(running)
        #pp(startup)
        diff = (running == startup)
        
        d[nxos]['start_running_match'] = diff
        d[nxos]['model'] = model
        d[nxos]['uptime'] = uptime
        d[nxos]['vendor'] = vendor
    pp(d)           

if __name__=="__main__":
    main()
