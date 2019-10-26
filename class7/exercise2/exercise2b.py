from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.core.filter import F
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result
import os

PASSWORD = os.environ.get("NORNIR_PASSWORD", None) # for testing purposes

def transform_ansible_inventory(host):
    host.password = PASSWORD or host["ansible_ssh_pass"]
    napalm_params = host.get_connection_parameters("napalm")
    if "nxos" in host.groups:
        napalm_params.platform = "nxos"
        napalm_params.port = 8443
    elif "cisco" in host.groups:
        napalm_params.platform = "ios"
    elif "arista" in host.groups:
        napalm_params.platform = "eos"
        napalm_params.extras["global_delay_factor"] = 2
    elif "juniper" in host.groups:
        napalm_params.platform = "junos"
    host.connection_options["napalm"] = napalm_params

def main():
    nr = InitNornir(config_file="config_b.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    agg_result = nr.run(task=napalm_get, getters=["facts"])

    print_result(agg_result)

if __name__=="__main__":
    main()
