#!/usr/bin/env python
# import general use modules
import os
import re
import time
from pprint import pprint as pp
# import nornir specifics
from nornir import InitNornir
from nornir.core.task import Result
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
from nornir.plugins.tasks import networking
from nornir.plugins.tasks import data
from nornir.plugins.tasks import text
from nornir.plugins.tasks import files
from nornir.plugins.tasks.networking import napalm_configure
from nornir.plugins.tasks.networking import napalm_get

def render_bgp_config(task):
    template_path = f"/home/petrache/nornir-course/class5/templates/{task.host.platform}/"
    template = "bgp.j2"
    result = task.run(task=text.template_file, template=template, path = template_path, **task.host)
    rendered_bgp = result[0].result
    task.host["rendered_bgp"] = rendered_bgp

def render_intf_config(task):
    template_path = f"/home/petrache/nornir-course/class5/templates/{task.host.platform}/"
    template = "interfaces.j2"
    result = task.run(task=text.template_file, template=template, path = template_path, **task.host)
    rendered_intf = result[0].result
    task.host["rendered_intf"] = rendered_intf

def write_bgp_config(task):
    cfg_path = f"/home/petrache/nornir-course/class5/rendered_configs/{task.host.platform}/"
    filename = f"{cfg_path}{task.host.name}_bgp"
    content = task.host["rendered_bgp"]
    result = task.run(task=files.write_file, filename=filename, content=content)

def write_intf_config(task):
    cfg_path = f"/home/petrache/nornir-course/class5/rendered_configs/{task.host.platform}/"
    filename = f"{cfg_path}{task.host.name}_interfaces"
    content = task.host["rendered_intf"]
    result = task.run(task=files.write_file, filename=filename, content=content)

def deploy_bgp_config(task):
    filename = f"/home/petrache/nornir-course/class5/rendered_configs/{task.host.platform}/{task.host.name}_bgp"
    with open(filename, "r") as f:
        bgp_cfg = f.read()
    result = task.run(task=networking.napalm_configure, configuration=bgp_cfg)

def deploy_intf_config(task):
    filename = f"/home/petrache/nornir-course/class5/rendered_configs/{task.host.platform}/{task.host.name}_interfaces"
    with open(filename, "r") as f:
        intf_cfg = f.read()
    result = task.run(task=networking.napalm_configure, configuration=intf_cfg)

def unitest_bgp(task):
    result = task.run(task=networking.napalm_get, getters=["bgp_neighbors"]) 



def main():
    
    nr = InitNornir(config_file="config5.yaml", logging={"enabled": False})
    nxos = nr.filter(F(groups__contains="nxos"))
    #import ipdb; ipdb.set_trace()
    
    render_bgp_result = nxos.run(task=render_bgp_config)
    print_result(render_bgp_result)
    render_intf_result = nxos.run(task=render_intf_config)
    print_result(render_intf_result)

    write_bgp_result = nxos.run(task=write_bgp_config)
    print_result(write_bgp_result)
    write_intf_result = nxos.run(task=write_intf_config)
    print_result(write_intf_result)

    deploy_bgp_result = nxos.run(task=deploy_bgp_config)
    print_result(deploy_bgp_result)
    deploy_intf_result = nxos.run(task=deploy_intf_config)
    print_result(deploy_intf_result)
    
    print("we now sleep for 10 seconds to ensure BGP processing is done")
    time.sleep(10)
     
    test_bgp = nxos.run(task=unitest_bgp)
    print_result(test_bgp)
    print("nxos1 bgp peer is UP ====>", test_bgp["nxos1"][1].result["bgp_neighbors"]["global"]["peers"]["172.20.1.2"]["is_up"])
    print("nxos2 bgp peer is UP ====>", test_bgp["nxos2"][1].result["bgp_neighbors"]["global"]["peers"]["172.20.1.1"]["is_up"])

if __name__=="__main__":
    main()

