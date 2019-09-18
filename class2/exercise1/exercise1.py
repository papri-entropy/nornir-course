#!/usr/bin/env python

from nornir import InitNornir

nr = InitNornir(config_file="config.yaml", core={"num_workers": 15})

number_workers = nr.config.core.num_workers

print(number_workers)

