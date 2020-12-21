import json
import csv
import copy

from Classes import *


def main():
    """sale_file = input("Unesite ime .json fajla sa salama: ")
    rok_file = input("Unesite ime .json fajla sa rokom: ")"""

    with open("javni_testovi\sale3.json", encoding="utf8", errors='ignore') as f:
        sale_json = json.load(f)

    with open("javni_testovi" + '\\' "rok3.json", encoding="utf8", errors='ignore') as f:
        rok_json = json.load(f)

    sale = [Sala(x['naziv'], x['kapacitet'], x['racunari'], x['dezurni'], x['etf'], i) for x in sale_json for i in
            range(4)]
    rok = Rok(rok_json['trajanje_u_danima'],
              [Ispit(x['sifra'], x['prijavljeni'], x['racunari'], x['odseci']) for x in rok_json['ispiti']])

    stanje = pocetnoStanje(rok, sale)

    for i in range(4):
        stanje.backtrack(0, i)

    #print(Stanje.rezultat)
    print("MIN POENI", Stanje.min_poeni)

    with open('raspored.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Dan1'] + ['sala' + sala.naziv for sala in sale if sala.termin == 0])
        for i in range(4):
            novi_red = []
            for _, sala in enumerate(sale):
                if sala.termin != i: continue
                to_append = [x for x in Stanje.rezultat if sala in x.sale]
                # print("SALA: ", sala.naziv + " " + mapaTermina[sala.termin])
                # print("TO APPEND: ", to_append)
                to_append = to_append[0].sifra_predmeta if len(to_append) == 1 else 'X'
                novi_red.append(to_append)
            writer.writerow(['T' + str(i + 1)] + novi_red)


def pocetnoStanje(rok, sale):
    Stanje.ispiti = [x for x in rok.ispiti]

    prosecan_kapacitet = 30 # utvrdjeno na osnovu javnih testova
    loss_function = lambda x: -((x.dezurni*x.kapacitet)/prosecan_kapacitet + (1.2 if not x.etf else 0))
    pocetni_domen = []
    for ispit in rok.ispiti:
        srtd = sorted([sala for sala in sale if ispit.racunari == sala.racunari],
                      key=loss_function) # sortiraj prema najmanjem skoru
        # print("SRTD: ", srtd)
        pocetni_domen.append(ElementDomena(ispit.sifra, srtd))

    return Stanje(pocetni_domen)


if __name__ == "__main__":
    main()
