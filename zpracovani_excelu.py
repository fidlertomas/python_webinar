import pandas as pd

df = pd.read_excel("MAC_adresy.xlsx")


def vyhledej_mac(mac):
    return df.loc[df["MAC adresa"].isin(mac)]
