#!/usr/bin/env python

# import general use modules
import os
from pprint import pprint as pp
# import nornir specifics
from nornir import InitNornir
from nornir.plugins.functions.text import print_result

nr = InitNornir()
hosts = nr.inventory.hosts
arista3_data = hosts['arista3'].data
arista3_items = hosts['arista3'].items()
print(hosts)
print(arista3_data)
print(arista3_items)

print(hosts['arista1']['timezone'])
print(hosts['arista2']['timezone'])
print(hosts['arista3']['timezone'])
