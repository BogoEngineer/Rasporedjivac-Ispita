import json
import csv
import copy

from Classes import *


def main():
    """sale_file = input("Unesite ime .json fajla sa salama: ")
    rok_file = input("Unesite ime .json fajla sa rokom: ")"""

    with open("javni_testovi\sale4.json", encoding="utf8", errors='ignore') as f:
        sale_json = json.load(f)

    with open("javni_testovi" + '\\' "rok4.json", encoding="utf8", errors='ignore') as f:
        rok_json = json.load(f)

    sale = [Sala(x['naziv'], x['kapacitet'], x['racunari'], x['dezurni'], x['etf'], i) for x in sale_json for i in
            range(4)]
    rok = Rok(rok_json['trajanje_u_danima'],
              [Ispit(x['sifra'], x['prijavljeni'], x['racunari'], x['odseci']) for x in rok_json['ispiti']])

    stanje = pocetnoStanje(rok, sale)

    rezultati_po_danima = []

    dan = 0
    while True:
        print("DAN: ", dan+1)
        print(stanje.domen)
        for i in range(4):
            stanje.backtrack(i, dan)

        rezultati_po_danima.append(Stanje.rezultat)
        if Stanje.finished: break

        rezultat = None
        min_poeni = sys.maxsize * 2 + 1  # max_int

        zavrseni_do_sad = []
        for elemDomena in stanje.domen:
            if elemDomena.dodeljeno:
                zavrseni_do_sad.append(elemDomena.sifra_predmeta)

        vadi_iz_roka = []
        for ispit in rok.ispiti:
            if ispit.sifra in zavrseni_do_sad:
                vadi_iz_roka.append(ispit)

        for ispit in vadi_iz_roka:
            rok.ispiti.remove(ispit)

        stanje = pocetnoStanje(rok, sale)
        dan += 1
        for elemDomena in stanje.domen:
            elemDomena.dan = dan

    print("REZULTATI:", rezultati_po_danima)
    #print(Stanje.rezultat)
    print("MIN POENI", Stanje.min_poeni, Stanje.id)

    with open('raspored.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for d in range(dan+1):
            writer.writerow(['Dan' + str(d+1)] + ['sala' + sala.naziv for sala in sale if sala.termin == 0])
            for i in range(4):
                novi_red = []
                for _, sala in enumerate(sale):
                    if sala.termin != i: continue
                    to_append = [x for x in rezultati_po_danima[d] if sala in x.sale]
                    # print("SALA: ", sala.naziv + " " + mapaTermina[sala.termin])
                    # print("TO APPEND: ", to_append)
                    to_append = to_append[0].sifra_predmeta if len(to_append) == 1 else 'X'
                    novi_red.append(to_append)
                writer.writerow(['T' + str(i + 1)] + novi_red)


def pocetnoStanje(rok, sale):
    Stanje.ispiti = [x for x in rok.ispiti]

    prosecan_kapacitet = 25 # utvrdjeno na osnovu javnih testova
    loss_function = lambda x: -((x.dezurni*x.kapacitet)/prosecan_kapacitet + (1.2 if not x.etf else 0))
    pocetni_domen = []
    for ispit in rok.ispiti:
        srtd = sorted([sala for sala in sale if ispit.racunari == sala.racunari],
                      key=loss_function) # sortiraj prema najmanjem skoru
        # print("SRTD: ", srtd)
        pocetni_domen.append(ElementDomena(ispit.sifra, srtd))

        broj_preostalih_mesta = [0 for i in range(4)]  # broj preostalih mesta u terminu
        for i in range(4):
            for sala in sale:
                if sala.termin != i: continue
                broj_preostalih_mesta[i] += sala.kapacitet

    return Stanje(pocetni_domen, broj_preostalih_mesta)


if __name__ == "__main__":
    main()
