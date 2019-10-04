#!/usr/bin/env python

# import general use modules
import os
import re
import time
from pprint import pprint as pp

# import nornir specifics
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
from nornir.plugins.tasks import networking
from nornir.plugins.tasks import text
from nornir.core.exceptions import NornirSubTaskError
from nornir.core.task import Result

# Custom Task To Render Interfaces Loopback Template
def render_loopback(task):
    template_path = f"/home/petrache/nornir-course/class6/exercise2/templates/{task.host.platform}/"
    template = "loopbacks.j2"
    try:
        task.run(task=text.template_file, template=template, path = template_path, **task.host)
        #print(result.result)
    except NornirSubTaskError:
        #print(dir(task))
        #print(task.results)
        print("Sad stuff man but we try to hide this exception")
        
        task.results.pop()
        
        msg = "Encountered Jinja2 error"
        return Result(
            changed=False,
            diff=None,
            result=msg,
            host=task.host,
            failed=False,
            exception=None,
        ) 

# Main Function Where We Run The Custom Task
def main():
    nr = InitNornir(config_file="config3.yaml", logging={"enabled": False})
    nxos = nr.filter(F(groups__contains="nxos"))

    render_loopback_result = nxos.run(task=render_loopback)
    #import ipdb; ipdb.set_trace()
    print_result(render_loopback_result)

if __name__=="__main__":
    main()
