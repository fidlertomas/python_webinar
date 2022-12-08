import netmiko
import re
import zpracovani_excelu


def konzole_vyber_z_moznosti(moznosti, co_vybiram):
    """procedura která na termál
    vypise moznosti a vrati vybranou moznost
    """
    print("Na výběr:")
    for i, moznost in enumerate(moznosti):
        print(f"{i} : {moznost}")
    vyber = int(input(f"Vyber {co_vybiram}:"))
    return moznosti[vyber]


def odblokuj_port(spojeni, port):
    prikazy = [f"int {port}", "shutdown", "no shutdown"]
    vystup = spojeni.send_config_set(prikazy)
    return vystup


def vytvor_spojeni(ip):
    popis_spojeni = {
        "ip": ip,
        "username": "admin",
        "password": "heslo",
        "device_type": "cisco_ios",
    }
    return netmiko.ConnectHandler(**popis_spojeni)


def vrat_err_dis_porty(spojeni):
    vystup = spojeni.send_command("show interfaces status err-disabled")
    print(vystup)
    porty = []
    for radek in vystup.splitlines():
        if "err-disabled" in radek:
            porty.append(re.search(f"^[\w/]+", radek)[0])
    return porty


switche = [
    "10.200.1.205",
    "10.200.1.204",
    "10.200.1.203",
    "10.200.1.202",
    "10.200.1.201",
]


vybrany_switch = konzole_vyber_z_moznosti(switche, "switch")
spojeni = vytvor_spojeni(vybrany_switch)
porty = vrat_err_dis_porty(spojeni)
if len(porty) == 0:
    exit()
port = konzole_vyber_z_moznosti(porty, "port ")

vystup = spojeni.send_command(f"sh port-security int {port} | in Last Source")

re_mac = r"[0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4}"
posledni_videna_mac = re.search(re_mac, vystup)[0]

print(f"Posleni videna MAC adresa na portu {port} byla {posledni_videna_mac}")

tabulka = zpracovani_excelu.vyhledej_mac(posledni_videna_mac)
if tabulka.shape[0] == 0:
    print("MAC nebyla v tabulce")
else:
    print(tabulka)

vystup = spojeni.send_command(f"sh port-security address | in  {port}")
alokovana_mac = re.search(re_mac, vystup)[0]
print(f"Spravna MAC adresa na portu {port} byla {alokovana_mac}")
tabulka = zpracovani_excelu.vyhledej_mac(alokovana_mac)
if tabulka.shape[0] == 0:
    print("MAC nebyla v tabulce")
else:
    print(tabulka)

if "A" == input("Chcete odblokovat port ? <A/N>"):
    print(odblokuj_port(spojeni, port))

spojeni.disconnect()
