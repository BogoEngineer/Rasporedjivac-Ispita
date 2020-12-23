import json
import csv
import copy

from Classes import *


def main():
    """sale_file = input("Unesite ime .json fajla sa salama: ")
    rok_file = input("Unesite ime .json fajla sa rokom: ")"""

    with open("javni_testovi\sale5.json", encoding="utf8", errors='ignore') as f:
        sale_json = json.load(f)

    with open("javni_testovi" + '\\' "rok5.json", encoding="utf8", errors='ignore') as f:
        rok_json = json.load(f)

    sale = [Sala(x['naziv'], x['kapacitet'], x['racunari'], x['dezurni'], x['etf'], i) for x in sale_json for i in
            range(4)]
    rok = Rok(rok_json['trajanje_u_danima'],
              [Ispit(x['sifra'], x['prijavljeni'], x['racunari'], x['odseci']) for x in rok_json['ispiti']])

    stanje = pocetnoStanje(rok, sale)
    # print("DOMEN 0: ", stanje.domen)
    rezultati_po_danima = []
    ukupni_poeni = 0

    dan = 0
    while True:
        print("DAN"+str(dan+1) + " PROSLEDJENO: ", len(stanje.domen))
        for i in range(4):
            stanje.backtrack(i, dan)

        rezultati_po_danima.append(copy.deepcopy(Stanje.rezultat))
        ukupni_poeni += copy.copy(Stanje.min_poeni)
        #print("DAN"+str(dan+1), len(Stanje.rezultat))
        #print([(x.sifra_predmeta, x.dodeljeno) for x in Stanje.rezultat])
        if Stanje.finished: break

        zavrseni_do_sad = []
        for elemDomena in Stanje.rezultat:
            if elemDomena.dodeljeno:
                zavrseni_do_sad.append(elemDomena.sifra_predmeta)

        vadi_iz_roka = []
        for ispit in rok.ispiti:
            if ispit.sifra in zavrseni_do_sad:
                vadi_iz_roka.append(ispit)

        for ispit in vadi_iz_roka:
            rok.ispiti.remove(ispit)

        stanje = pocetnoStanje(rok, sale)
        # print("DOMEN "+str(dan+1)+": ", stanje.domen)
        dan += 1
        for elemDomena in stanje.domen:
            # print(elemDomena.sifra_predmeta, dan)
            elemDomena.dan = dan

    #for i,rpd in enumerate(rezultati_po_danima):
    #    print("ZA DAN "+str(i+1))
    #    print([x.sifra_predmeta for x in rpd if x.dodeljeno])

    #print("REZULTAT: ", rezultati_po_danima)

    print("MIN POENI", ukupni_poeni)

    with open('raspored.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for d in range(dan+1):
            writer.writerow(['Dan' + str(d+1)] + ['sala' + sala.naziv for sala in sale if sala.termin == 0])
            for i in range(4):
                novi_red = []
                for _, sala in enumerate(sale):
                    if sala.termin != i: continue
                    to_append = [x for x in rezultati_po_danima[d] if sala in x.sale and x.dodeljeno]
                    # print("SALA: ", sala.naziv + " " + mapaTermina[sala.termin])
                    # print("TO APPEND: ", to_append)
                    to_append = to_append[0].sifra_predmeta if len(to_append) == 1 else 'X'
                    novi_red.append(to_append)
                writer.writerow(['T' + str(i + 1)] + novi_red)


def pocetnoStanje(rok, sale):
    Stanje.rezultat = None
    Stanje.min_poeni = sys.maxsize * 2 + 1  # max_int
    Stanje.ispiti = [x for x in rok.ispiti]

    prosecan_kapacitet = 25 # utvrdjeno na osnovu javnih testova
    loss_function = lambda x: -((x.dezurni*x.kapacitet)/prosecan_kapacitet + (1.2 if not x.etf else 0))
    pocetni_domen = []
    for ispit in rok.ispiti:
        srtd = sorted([sala for sala in sale if ispit.racunari == sala.racunari],
                      key=loss_function) # sortiraj prema najmanjem skoru
        # print("SRTD: ", srtd)
        pocetni_domen.append(ElementDomena(ispit.sifra, srtd))

    #broj_preostalih_mesta = [0 for i in range(4)]  # broj preostalih mesta u terminu
    """for i in range(4):
        for sala in sale:
            if sala.termin != i: continue
            broj_preostalih_mesta[i] += sala.kapacitet"""

    return Stanje(pocetni_domen)


if __name__ == "__main__":
    main()
