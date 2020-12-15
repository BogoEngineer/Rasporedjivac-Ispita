import json
import csv

from Classes import *


def main():
    """sale_file = input("Unesite ime .json fajla sa salama: ")
    rok_file = input("Unesite ime .json fajla sa rokom: ")"""

    with open("javni_testovi\sale1.json", encoding="utf8", errors='ignore') as f:
        sale_json = json.load(f)

    with open("javni_testovi" +'\\' "rok1.json", encoding="utf8", errors='ignore') as f:
        rok_json = json.load(f)

    sale = [Sala(x['naziv'], x['kapacitet'], x['racunari'], x['dezurni'], x['etf']) for x in sale_json]
    rok = Rok(rok_json['trajanje_u_danima'],
              [Ispit(x['sifra'], x['prijavljeni'], x['racunari'], x['odseci']) for x in rok_json['ispiti']])
    print(sale)
    print(rok)


if __name__ == "__main__":
    main()
