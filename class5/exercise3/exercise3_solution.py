from nornir import InitNornir
from nornir.plugins.tasks import data
from nornir.plugins.functions.text import print_result
from pprint import pprint as pp

def junos_acl(task):

    # Load the YAML-ACL entries
    in_yaml = task.run(task=data.load_yaml, file=f"acl.yaml")
    in_yaml = in_yaml[0].result
    rules = []

    for acl_name, acl_entries in in_yaml.items():
        print(acl_name, acl_entries, "NEXT PRINTING ACL_ENTRY")
        for acl_entry in acl_entries:
            print(acl_entry)
            rules.append(
                f"set firewall family inet filter {acl_name} term {acl_entry['term_name']} "
                f"from protocol {acl_entry['protocol']}"
            )
            rules.append(
                f"set firewall family inet filter {acl_name} term {acl_entry['term_name']} "
                f"from destination-port {acl_entry['destination_port']}"
            )
            rules.append(
                f"set firewall family inet filter {acl_name} term {acl_entry['term_name']} "
                f"from destination-address {acl_entry['destination_address']}"
            )
            rules.append(
                f"set firewall family inet filter {acl_name} term {acl_entry['term_name']} "
                f"then {acl_entry['state']}"
            )

    print()
    print("#" * 80)
    for rule in rules:
        print(rule)
    print("#" * 80)
    print()


def main():
    nr = InitNornir(config_file="config3.yaml")
    nr = nr.filter(name="srx2")
    result = nr.run(task=junos_acl)
    print_result(result)

if __name__ == "__main__":
    main()
