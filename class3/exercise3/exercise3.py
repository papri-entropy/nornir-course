#!/usr/bin/env python

# import general use modules
import os
from pprint import pprint as pp
# import nornir specifics
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F

def main():
    nr = InitNornir()
    hosts = nr.inventory.hosts

    print(hosts)

    agg_filter = nr.filter(F(role="AGG"))
    agg_filter = agg_filter.inventory.hosts

    print(agg_filter)

    union_filter = nr.filter(F(groups__contains="sea") | F(groups__contains="sfo"))
    union_filter = union_filter.inventory.hosts

    print(union_filter)

    intersect_filter = nr.filter(F(role="WAN") & F(site_details__wifi_password__contains="racecar"))
    intersect_filter = intersect_filter.inventory.hosts

    print(intersect_filter)

    negate_filter = nr.filter(F(role="WAN") & ~F(site_details__wifi_password__contains="racecar"))
    negate_filter = negate_filter.inventory.hosts

    print(negate_filter)


if __name__=="__main__":
    main()
