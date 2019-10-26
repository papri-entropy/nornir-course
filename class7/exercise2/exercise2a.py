from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.core.filter import F
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result
import os

PASSWORD = os.environ.get("NORNIR_PASSWORD", None) # for testing purposes

def transform_ansible_inventory(host):
    host.password = PASSWORD or host["ansible_ssh_pass"]
    netmiko_params = host.get_connection_parameters("netmiko")
    if "nxos" in host.groups:
        netmiko_params.platform = "cisco_nxos"
    elif "cisco" in host.groups:
        netmiko_params.platform = "cisco_ios"
    elif "arista" in host.groups:
        netmiko_params.platform = "arista_eos"
        netmiko_params.extras["global_delay_factor"] = 2
    elif "juniper" in host.groups:
        netmiko_params.platform = "juniper_junos"
    host.connection_options["netmiko"] = netmiko_params

def main():
    nr = InitNornir(config_file="config_a.yaml")
    nr = nr.filter(F(groups__contains="cisco") | F(groups__contains="arista") | F(groups__contains="juniper") | F(groups__contains="nxos"))
    agg_result = nr.run(task=networking.netmiko_send_command, command_string="show version")
    print_result(agg_result)

if __name__=="__main__":
    main()
