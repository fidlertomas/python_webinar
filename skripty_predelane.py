import netmiko
import time
import re
import zpracovani_excelu

switche = [
    "10.200.1.205",
    "10.200.1.204",
    "10.200.1.203",
    "10.200.1.202",
    "10.200.1.201",
]


def konzole_vyber_z_moznosti(moznosti, co_vybiram):
    """procedura která na termál
    vypise moznosti a vrati vybranou moznost
    """
    print("Na výběr:")
    for i, moznost in enumerate(moznosti):
        print(f"{i} : {moznost}")
    vyber = int(input(f"Vyber {co_vybiram}:"))
    return moznosti[vyber]


def pripojit(ip_zarizeni):
    parametry_spojeni = {
        "ip": ip_zarizeni,
        "username": "admin",
        "password": "heslo",
        "device_type": "cisco_ios",
    }
    return netmiko.ConnectHandler(**parametry_spojeni)


def vypis_podrobnosti(spojeni, port):
    reg_mac = r"[0-9a-f]{4}.[0-9a-f]{4}.[0-9a-f]{4}"
    vystup = spojeni.send_command(
        f"show port-security int {port} | include Last Source"
    )
    mac = re.findall(reg_mac, vystup)
    navratova_hodnota = f"posledni viděná adresa na portu {port} byla : {mac}" + "\n"

    radek_z_tabulky = zpracovani_excelu.vyhledej_mac(mac)
    if radek_z_tabulky.shape[0] == 0:
        navratova_hodnota += str("MAC adresa není v seznamu.") + "\n"
    else:
        navratova_hodnota += str(radek_z_tabulky) + "\n"

    vystup = spojeni.send_command(f"show port-security address | in {port}")
    mac = re.findall(reg_mac, vystup)
    navratova_hodnota += str(f"MAC adresa spravně na portu je : {mac}") + "\n"
    radek_z_tabulky = zpracovani_excelu.vyhledej_mac(mac)
    if radek_z_tabulky.shape[0] == 0:
        navratova_hodnota += str("MAC adresa není v seznamu.") + "\n"
    else:
        navratova_hodnota += str(radek_z_tabulky) + "\n"

    return navratova_hodnota


def odblokovani_portu(spojeni, port):
    prikazy = [f"interface {port}", "shutdown", "no shutdown"]
    return spojeni.send_config_set(prikazy)


def vypis_error_disable(switch):
    spojeni = pripojit(switch)
    vystup = spojeni.send_command("show interface status err-disable")
    spojeni.disconnect()
    return vystup


def vypis_podrobnosti_error_disable(switch):
    spojeni = pripojit(switch)
    vystup = spojeni.send_command("show interface status err-disable")
    porty = []
    vystupy = dict()
    for line in vystup.splitlines():
        if "err-disabled" in line:
            porty.append(re.search(r"(^[\w\/]+)\w", line)[0])
    if len(porty) == 0:
        return None
    for port in porty:
        vystupy[port] = vypis_podrobnosti(spojeni, port)
    spojeni.disconnect()
    return vystupy


def odblokuj_port(ip, port):
    spojeni = pripojit(ip)
    print(odblokovani_portu(spojeni, port))


if __name__ == "__main__":
    try:

        switch = konzole_vyber_z_moznosti(switche, "switch")

        spojeni = pripojit(switch)
        vystup = spojeni.send_command("show interface status err-disable")
        print(vystup)
        porty = []
        for line in vystup.splitlines():
            if "err-disabled" in line:
                porty.append(re.search(r"(^[\w\/]+)\w", line)[0])
        if len(porty) == 0:
            exit()
        rozhrani = konzole_vyber_z_moznosti(porty, "port")
        print(vypis_podrobnosti(spojeni, rozhrani))

        if "A" == input("Chcete odblokovat port? (A/N):"):
            print(odblokovani_portu(spojeni, rozhrani))
            time.sleep(5)
            print("porty které zůstaly zablokované:")
            print(spojeni.send_command("show interface status err-disable"))

    finally:
        spojeni.disconnect()
