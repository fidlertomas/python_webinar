import netmiko
import re


def konzole_vyber_z_moznosti(moznosti, co_vybiram):
    """procedura která na termál
    vypise moznosti a vrati vybranou moznost
    """
    print("Na výběr:")
    for i, moznost in enumerate(moznosti):
        print(f"{i} : {moznost}")
    vyber = int(input(f"Vyber {co_vybiram}:"))
    return moznosti[vyber]


switche = [
    "10.200.1.205",
    "10.200.1.204",
    "10.200.1.203",
    "10.200.1.202",
    "10.200.1.201",
]


vybrany_switch = konzole_vyber_z_moznosti(switche, "switch")


popis_spojeni = {
    "ip": vybrany_switch,
    "username": "admin",
    "password": "heslo",
    "device_type": "cisco_ios",
}


spojeni = netmiko.ConnectHandler(**popis_spojeni)

vystup = spojeni.send_command("show interfaces status err-disabled")
print(vystup)
porty = []
for radek in vystup.splitlines():
    if "err-disabled" in radek:
        porty.append(re.search(f"^[\w/]+", radek)[0])

if len(porty) == 0:
    exit()

port = konzole_vyber_z_moznosti(porty, "port ")
prikazy = [f"int {port}", "shutdown", "no shutdown"]
vystup = spojeni.send_config_set(prikazy)
print("#" * 10)
print(vystup)

spojeni.disconnect()
