from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result
import os

# Set this env variable for the script to succeed
#NORNIR_INVENTORY_TRANSFORM_FUNCTION=exercise1b.transform_set_password 

def transform_set_password(host):
    host.password = os.environ.get("NORNIR_PASSWORD", "bogus")

def main():
    nr = InitNornir(config_file="config.yaml")
    #import ipdb; ipdb.set_trace()
    #print(f"{nr.inventory.hosts['nxos1'].password}") 
        
    for host, host_obj in nr.inventory.hosts.items():
        if "nxos" in host:
            napalm_params = host_obj.get_connection_parameters("napalm")
            #print(napalm_params.port)
            host_obj.connection_options["napalm"] = napalm_params
    #print(napalm_params.dict())
    
    agg_result = nr.run(task=networking.napalm_get, getters=["ntp_servers"])
    print_result(agg_result)

if __name__=="__main__":
    main()
