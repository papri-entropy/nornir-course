from nornir import InitNornir
from nornir.plugins.tasks import networking

def main():
    nr = InitNornir(config_file="config.yaml")
    #import ipdb; ipdb.set_trace()
    nxos1 = nr.inventory.hosts["nxos1"]    
    print(nxos1.username, nxos1.password, nxos1.platform, nxos1.port)    
    print(nxos1.get_connection_parameters("napalm").port)
     
if __name__=="__main__":
    main()
