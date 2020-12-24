import sys
import copy

mapaTermina = {
    0: "8:00",
    1: "11:30",
    2: "15:00",
    3: "18:30"
}


class Sala:
    def __init__(self, naziv, kapacitet, racunari, dezurni, etf, termin):
        self.naziv = naziv
        self.kapacitet = kapacitet
        self.racunari = (racunari == 1)
        self.dezurni = dezurni
        self.etf = (etf == 1)
        self.termin = termin

    def __str__(self):
        return "naziv: " + self.naziv + \
               " kapacitet: " + str(self.kapacitet) + \
               " racunari:  " + str(self.racunari) + \
               " dezurni: " + str(self.dezurni) + \
               " etf: " + str(self.etf) + \
               " termin: " + str(mapaTermina[self.termin])

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.naziv == other.naziv and self.termin == other.termin


class Rok:
    def __init__(self, trajanje_u_danima, ispiti):
        self.trajanje_u_danima = trajanje_u_danima
        self.ispiti = ispiti

    def __str__(self):
        return "trajanje: " + str(self.trajanje_u_danima) \
               + "ispiti: " + str(self.ispiti)


class Ispit:
    def __init__(self, sifra, prijavljeni, racunari, odseci):
        self.sifra = sifra
        self.prijavljeni = prijavljeni
        self.racunari = (racunari == 1)
        self.odseci = odseci
        self.godina = -1
        for c in sifra[-2::-1]:
            if str(c).isdigit():
                self.godina = int(c)
                break

    def __str__(self):
        return "sifra: " + self.sifra + \
               " prijavljeni: " + str(self.prijavljeni) + \
               " racunari: " + str(self.racunari) + \
               " odseci: " + str(self.odseci)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return other.sifra == self.sifra


class ElementDomena:
    def __init__(self, sifra_predmeta, sale):
        self.sifra_predmeta = sifra_predmeta
        self.dodeljeno = False
        self.sale = sale  # predstavlja sale koje su u opticaju ako je dodeljeno == False, u suprotnom odabrane sale
        self.dan = 0
        self.valid = True  # da li sme ispit da se odrzi danas (u slucaju da je stavljen vec u raspored neki drugi ispit
        # koji je ista godina na istom smeru)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Sifra_predmeta: " + self.sifra_predmeta + \
               " Dodeljeno: " + str(self.dodeljeno) + \
               " Dan: " + str(self.dan) + \
               " Sale: " + str(self.sale)

    def __eq__(self, other):
        return self.sifra_predmeta == other.sifra_predmeta

class Stanje:
    id = 0
    rezultat = None  # rezultat za jedan dan
    min_poeni = sys.maxsize * 2 + 1  # max_int
    min_id = -1
    finished = False
    ispiti = []

    def __init__(self, domen):
        self.domen = domen
        self.id = Stanje.id
        Stanje.id += 1
        # self.broj_preostalih_mesta = preostala_mesta

    def __str__(self):
        return "Domen: " + str(self.domen)

    def backtrack(self, termin, dan):
        # print("SAVADE"+ str(termin))
        nedodeljeni = [x for x in self.domen if not x.dodeljeno and x.valid] # nedodeljeni a validni za ovaj dan
        if len(nedodeljeni) > 0:  # ako nije zavrseno sa dodelom sala za sve ispite
            ima_mesta = []  # AKO NEMA MESTA U OVOM TERMINU ZAOVI BACKTRACK ZA SLEDECE PA VIDI TU, NE ODUSTAJ ODMAH!!!
            for elemDomena in nedodeljeni:
                ispit = self.nadjiIspitPoSifri(elemDomena.sifra_predmeta)
                potrebno = ispit.prijavljeni
                for sala in elemDomena.sale:
                    if sala.termin != termin: continue
                    potrebno -= sala.kapacitet

                if potrebno <= 0: ima_mesta.append(elemDomena)
            if len(ima_mesta) == 0:  # ako nema mesta vise u ovom terminu za bilo koji od nedodeljenih isppita
                if termin != 3:  # probaj da nadjes mesta za ispit u narednom terminu
                    Stanje(copy.deepcopy(self.domen)).backtrack(termin + 1, dan)
                potencijalni_poeni = self.izracunajLoss()
                if Stanje.rezultat is None:
                    Stanje.rezultat = self.domen
                    Stanje.min_poeni = potencijalni_poeni
                else:
                    if len([x for x in self.domen if x.dodeljeno]) > len([x for x in Stanje.rezultat if x.dodeljeno]):
                        Stanje.rezultat = self.domen
                        Stanje.min_poeni = potencijalni_poeni
                    elif len([x for x in self.domen if x.dodeljeno]) == len(
                            [x for x in Stanje.rezultat if x.dodeljeno]):
                        Stanje.rezultat = self.domen if potencijalni_poeni < Stanje.min_poeni else Stanje.rezultat
                        Stanje.min_poeni = potencijalni_poeni if potencijalni_poeni < Stanje.min_poeni else Stanje.min_poeni

                return
            else:  # ima mesta u ovom terminu za dodeljivanje mesta ispitima
                sledeca_promenljiva = min(ima_mesta,
                                          key=lambda d: len(d.sale))
                # sledeci ispit se bira na osnovu toga koliko sala u opticaju ima (zaobilazenje nepotrebnih konflikata)
                # ali za koju ima mesta
                sledeci_ispit = next((x for x in Stanje.ispiti if x.sifra == sledeca_promenljiva.sifra_predmeta), None)
                smesteni_stuednti = 0
                temp_sale = []
                while smesteni_stuednti < sledeci_ispit.prijavljeni:
                    if len(sledeca_promenljiva.sale) == 0: return
                    sledeca_sala = next((sala for sala in sledeca_promenljiva.sale if sala.termin == termin),
                                        None)  # sale su
                    # sortirane prema broju dezurnih i
                    # tome da li su na etfu ili ne, respektivno
                    sledeca_promenljiva.sale.remove(sledeca_sala)
                    smesteni_stuednti += sledeca_sala.kapacitet
                    temp_sale.append(sledeca_sala)

                sledeca_promenljiva.dodeljeno = True
                sledeca_promenljiva.sale = temp_sale

                trenutni_poeni = self.izracunajLoss()
                if trenutni_poeni >= Stanje.min_poeni: return  # optimizacija

                self.forward_check(temp_sale, sledeca_promenljiva)

                Stanje(copy.deepcopy(self.domen)).backtrack(termin, dan)
        else:  # ako je zavrseno sa dodelom sala za sve ispite
            if len([x for x in self.domen if not x.dodeljeno and not x.valid]) == 0:
                Stanje.finished = True  # svim ispitima je dodeljen termin i nema termina preostalih za naredne dane
            potencijalni_poeni = self.izracunajLoss()
            Stanje.rezultat = self.domen if potencijalni_poeni < Stanje.min_poeni else Stanje.rezultat
            Stanje.min_poeni = potencijalni_poeni if potencijalni_poeni < Stanje.min_poeni else Stanje.min_poeni
            # Stanje.id = self.id
            return

    def forward_check(self, uzete_sale, postavljen_ispit):
        ispit_objekat = self.nadjiIspitPoSifri(postavljen_ispit.sifra_predmeta)
        for elem in self.domen:
            if elem.dodeljeno: continue
            for sala in uzete_sale:
                if sala in elem.sale: elem.sale.remove(sala)

        # forward checking za istu godinu i smer
        mapa_smerova = {}
        for elem in self.domen:
            if elem == postavljen_ispit: continue
            ispit = self.nadjiIspitPoSifri(elem.sifra_predmeta)
            for odsek in ispit.odseci:
                if odsek not in mapa_smerova:
                    mapa_smerova[odsek] = [elem]
                else:
                    mapa_smerova[odsek].append(elem)

        for odsek in self.nadjiIspitPoSifri(postavljen_ispit.sifra_predmeta).odseci:
            if odsek in mapa_smerova:
                for elem in mapa_smerova[odsek]:
                    trenutni_ispit = self.nadjiIspitPoSifri(elem.sifra_predmeta)
                    # uslov za ispite istih godina i smerova u jednom danu
                    if trenutni_ispit.godina == ispit_objekat.godina:
                        elem.valid = False
                    # uslov za ispite susednih godina i istih smerova u istom terminu
                    elif abs(trenutni_ispit.godina - ispit_objekat.godina) == 1:
                        temp_remove = []
                        for sala in elem.sale:
                            if sala.termin == postavljen_ispit.sale[0].termin: temp_remove.append(sala)

                        for to_remove in temp_remove:
                            elem.sale.remove(to_remove)

    def izracunajLoss(self):
        ret = 0
        for elem in self.domen:
            if not elem.dodeljeno: continue
            for sala in elem.sale:
                ret += sala.dezurni + (1.2 if not sala.etf else 0)

        return ret

    def nadjiIspitPoSifri(self, sifra):
        return [x for x in Stanje.ispiti if x.sifra == sifra][0]
