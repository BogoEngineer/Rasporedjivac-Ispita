
class Sala:
    def __init__(self, naziv, kapacitet, racunari, dezurni, etf):
        self.naziv = naziv
        self.kapacitet = kapacitet
        self.racunari = (racunari == 1)
        self.dezurni = dezurni
        self.etf = (etf==1)

    def __str__(self):
        return "naziv: "+self.naziv+" kapacitet: "+str(self.kapacitet)+" racunari:  "+str(self.racunari)+" dezurni: "+str(self.dezurni)+" etf:"+str(self.etf)

    def __repr__(self):
        return str(self)
class Rok:
    def __init__(self, trajanje_u_danima, ispiti):
        self.trajanje_u_danima = trajanje_u_danima
        self.ispiti = ispiti

    def __str__(self):
        return "trajanje: "+str(self.trajanje_u_danima)+"ispiti: "+str(self.ispiti)

class Ispit:
    def __init__(self, sifra, prijavljeni, racunari, odseci):
        self.sifra = sifra
        self.prijavljeni = prijavljeni
        self.racunari = (racunari == 1)
        self.odseci = odseci

    def __str__(self):
        return "sifra: "+self.sifra+" prijavljeni: "+str(self.prijavljeni)+" racunari: "+str(self.racunari)+" odseci: "+str(self.odseci)

    def __repr__(self):
        return str(self)