from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result

def netmiko_direct(task):
    print(task.host.username)
    # Manually create Netmiko connection
    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    print()
    print("#" * 80)
    print(net_connect.find_prompt())
    print("#" * 80)
    print()


if __name__=="__main__":
    nr = InitNornir(config_file="config.yaml")
    result = nr.run(task=netmiko_direct, num_workers=1)
    print_result(result)
