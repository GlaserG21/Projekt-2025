from datetime import datetime

class Auto:
    def __init__(self, rendszam, tipus, ar):
        self.rendszam = rendszam
        self.tipus = tipus
        self.ar = ar
        self.foglalt_datumok = []

    def szabad_e(self, datum):
        return datum not in self.foglalt_datumok

    def berel(self, datum):
        if self.szabad_e(datum):
            self.foglalt_datumok.append(datum)
            return self.ar
        else:
            return 0

    def lemond(self, datum):
        if datum in self.foglalt_datumok:
            self.foglalt_datumok.remove(datum)
            return True
        return False

class Szemelyauto(Auto):
    def __init__(self, rendszam, tipus, ar, ulesek_szama):
        super().__init__(rendszam, tipus, ar)
        self.ulesek_szama = ulesek_szama

class Teherauto(Auto):
    def __init__(self, rendszam, tipus, ar, teherbiras):
        super().__init__(rendszam, tipus, ar)
        self.teherbiras = teherbiras

class Berles:
    def __init__(self, auto, datum):
        self.auto = auto
        self.datum = datum
        self.ar = auto.ar

class Kolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def hozzaad_auto(self, auto):
        self.autok.append(auto)

    def keres_auto(self, rendszam):
        for a in self.autok:
            if a.rendszam == rendszam:
                return a
        return None

    def berel_auto(self, rendszam, datum):
        auto = self.keres_auto(rendszam)
        if auto is not None and auto.szabad_e(datum):
            ar = auto.berel(datum)
            b = Berles(auto, datum)
            self.berlesek.append(b)
            return f"Bérlés sikeres: {ar} Ft"
        return "Nem sikerült a bérlés. Lehet, hogy az autó nem létezik vagy foglalt."

    def lemond_berlest(self, rendszam, datum):
        auto = self.keres_auto(rendszam)
        if auto and auto.lemond(datum):
            for b in self.berlesek:
                if b.auto == auto and b.datum == datum:
                    self.berlesek.remove(b)
                    return "Bérlés lemondva."
        return "Nem sikerült lemondani."

    def listaz_berlesek(self):
        if not self.berlesek:
            return "Nincsenek bérlések."
        szoveg = ""
        for b in self.berlesek:
            szoveg += f"{b.auto.rendszam} - {b.auto.tipus} - {b.datum} - {b.ar} Ft\n"
        return szoveg

    def listaz_berelheto_autok(self, datum):
        lista = []
        for auto in self.autok:
            if auto.szabad_e(datum):
                lista.append(f"{auto.rendszam} - {auto.tipus} - {auto.ar} Ft/nap")
        if lista:
            return "\n".join(lista)
        else:
            return "Nincs szabad autó ezen a napon."

def datum_bekeres():
    s = input("Add meg a dátumot (ÉÉÉÉ-HH-NN): ")
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except:
        return None

def main():
    k = Kolcsonzo("Teszt Kölcsönző")
    k.hozzaad_auto(Szemelyauto("AAA-111", "Opel", 10000, 5))
    k.hozzaad_auto(Teherauto("BBB-222", "MAN", 20000, 3000))

    while True:
        print("\n1. Autó bérlése")
        print("2. Bérlés lemondása")
        print("3. Bérlések listázása")
        print("4. Bérelhető autók listázása adott napra")
        print("5. Kilépés")
        val = input("Választás: ")

        if val == "1":
            rendszam = input("Rendszám: ")
            datum = datum_bekeres()
            if datum:
                print(k.berel_auto(rendszam, datum))
            else:
                print("Hibás dátum.")
        elif val == "2":
            rendszam = input("Rendszám: ")
            datum = datum_bekeres()
            if datum:
                print(k.lemond_berlest(rendszam, datum))
            else:
                print("Hibás dátum.")
        elif val == "3":
            print(k.listaz_berlesek())
        elif val == "4":
            datum = datum_bekeres()
            if datum:
                print(k.listaz_berelheto_autok(datum))
            else:
                print("Hibás dátum.")
        elif val == "5":
            print("Kilépés...")
            break
        else:
            print("Érvénytelen opció.")

if __name__ == "__main__":
    main()
