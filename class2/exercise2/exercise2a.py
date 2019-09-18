#!/usr/bin/env python

from pprint import pprint as pp

from nornir import InitNornir

nr = InitNornir(config_file="config.yaml")

nr = nr.filter(platform="ios")

pp(nr.inventory.hosts)
