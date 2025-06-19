from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Auto(ABC):
    def __init__(self, rendszam, tipus, berleti_dij):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij
        self.foglalt_napok = []
    
    @abstractmethod
    def get_tipus(self):
        pass
    
    def szabad_e(self, datum):
        return datum not in self.foglalt_napok
    
    def berel(self, datum):
        if self.szabad_e(datum):
            self.foglalt_napok.append(datum)
            return self.berleti_dij
        return 0
    
    def lemond(self, datum):
        if datum in self.foglalt_napok:
            self.foglalt_napok.remove(datum)
            return True
        return False

class Szemelyauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, ulesek_szama, klima):
        super().__init__(rendszam, tipus, berleti_dij)
        self.ulesek_szama = ulesek_szama
        self.klima = klima
    
    def get_tipus(self):
        return "Személyautó"

class Teherauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, teherbiras, hidraulikus):
        super().__init__(rendszam, tipus, berleti_dij)
        self.teherbiras = teherbiras
        self.hidraulikus = hidraulikus
    
    def get_tipus(self):
        return "Teherautó"

class Berles:
    def __init__(self, auto, datum):
        self.auto = auto
        self.datum = datum
        self.ar = auto.berleti_dij

class Autokolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.autok = []
        self.berlesek = []
    
    def auto_hozzaad(self, auto):
        self.autok.append(auto)
    
    def auto_keres(self, rendszam):
        for auto in self.autok:
            if auto.rendszam == rendszam:
                return auto
        return None
    
    def berel(self, rendszam, datum):
        auto = self.auto_keres(rendszam)
        if auto and auto.szabad_e(datum):
            ar = auto.berel(datum)
            if ar > 0:
                berles = Berles(auto, datum)
                self.berlesek.append(berles)
                return True, f"Sikeres bérlés! Ár: {ar} Ft"
            return False, "Az autó ezen a napon már foglalt."
        return False, "Az autó nem található vagy foglalt."
    
    def lemond(self, rendszam, datum):
        auto = self.auto_keres(rendszam)
        if auto:
            if auto.lemond(datum):
                for berles in self.berlesek:
                    if berles.auto == auto and berles.datum == datum:
                        self.berlesek.remove(berles)
                        break
                return True, "Sikeres lemondás!"
            return False, "Nincs ilyen bérlés."
        return False, "Az autó nem található."
    
    def get_berlesek(self):
        return self.berlesek
    
    def get_autok(self):
        return self.autok
    
    def get_szabad_autok(self, datum=None):
        if datum is None:
            datum = datetime.now().date()
        return [auto for auto in self.autok if auto.szabad_e(datum)]
    
    def get_foglalt_autok(self, datum=None):
        if datum is None:
            datum = datetime.now().date()
        return [auto for auto in self.autok if not auto.szabad_e(datum)]
    
    def autok_listaz(self):
        if not self.autok:
            return "Nincsenek autók a rendszerben."
        
        eredmeny = "Összes autó:\n"
        for auto in self.autok:
            statusz = "Szabad" if not auto.foglalt_napok else "Foglalt"
            foglalt_napok_szama = len(auto.foglalt_napok)
            eredmeny += (f" - Rendszám: {auto.rendszam}, "
                        f"Típus: {auto.get_tipus()}, "
                        f"Díj: {auto.berleti_dij} Ft/nap, "
                        f"Státusz: {statusz}")
            
            if foglalt_napok_szama > 0:
                foglalt_datumok = ", ".join([d.strftime('%Y-%m-%d') for d in sorted(auto.foglalt_napok)])
                eredmeny += f", Foglalt napok: {foglalt_napok_szama} [{foglalt_datumok}]"
            
            eredmeny += "\n"
        return eredmeny
    
    def berlesek_listaz(self):
        if not self.berlesek:
            return "Nincsenek aktív bérlések."
        
        eredmeny = "Aktív bérlések:\n"
        for i, berles in enumerate(self.berlesek, 1):
            eredmeny += (f"{i}. Rendszám: {berles.auto.rendszam}, "
                        f"Típus: {berles.auto.get_tipus()}, "
                        f"Dátum: {berles.datum.strftime('%Y-%m-%d')}, "
                        f"Ár: {berles.ar} Ft\n")
        return eredmeny
    
    def berelheto_autok_listaz(self, datum=None):
        if datum is None:
            datum = datetime.now().date()
        
        szabad_autok = self.get_szabad_autok(datum)
        foglalt_autok = self.get_foglalt_autok(datum)
        
        eredmeny = f"\n=== Bérelhető autók ({datum.strftime('%Y-%m-%d')}) ===\n"
        
        eredmeny += "\nSzabad autók:\n"
        if szabad_autok:
            for auto in szabad_autok:
                eredmeny += (f" - Rendszám: {auto.rendszam}, "
                            f"Típus: {auto.get_tipus()}, "
                            f"Díj: {auto.berleti_dij} Ft/nap\n")
        else:
            eredmeny += " - Nincsenek szabad autók\n"
        
        eredmeny += "\nFoglalt autók:\n"
        if foglalt_autok:
            for auto in foglalt_autok:
                eredmeny += (f" - Rendszám: {auto.rendszam}, "
                            f"Típus: {auto.get_tipus()}\n")
        else:
            eredmeny += " - Nincsenek foglalt autók\n"
        
        return eredmeny

def inicializalas():
    kolcsonzo = Autokolcsonzo("Jó Autók Kft.")
    
    kolcsonzo.auto_hozzaad(Szemelyauto("ABC-123", "Toyota Corolla", 15000, 5, True))
    kolcsonzo.auto_hozzaad(Szemelyauto("DEF-456", "Opel Astra", 12000, 5, False))
    kolcsonzo.auto_hozzaad(Teherauto("GHI-789", "Volvo FH", 30000, 20000, True))
    kolcsonzo.auto_hozzaad(Szemelyauto("JKL-012", "Ford Focus", 18000, 5, True))
    kolcsonzo.auto_hozzaad(Teherauto("MNO-345", "MAN TGX", 35000, 25000, False))
    
    return kolcsonzo

def felhasznaloi_interfesz():
    kolcsonzo = inicializalas()
    
    while True:
        print("\n" + "="*50)
        print("=== Autókölcsönző Rendszer - Minden autó szabad ===")
        print("="*50)
        print("1. Összes autó listázása")
        print("2. Bérelhető autók listázása (dátum szerint)")
        print("3. Autó bérlése")
        print("4. Bérlés lemondása")
        print("5. Aktív bérlések megtekintése")
        print("6. Kilépés")
        
        try:
            valasztas = input("\nVálasszon egy menüpontot (1-6): ")
            
            if valasztas == "1":
                print("\n" + kolcsonzo.autok_listaz())
            
            elif valasztas == "2":
                while True:
                    datum_str = input("\nAdja meg a dátumot (ÉÉÉÉ-HH-NN, üresen hagyva a mai nap): ").strip()
                    if not datum_str:
                        datum = datetime.now().date()
                        break
                    try:
                        datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
                        break
                    except ValueError:
                        print("Hibás dátumformátum! Használja az ÉÉÉÉ-HH-NN formátumot.")
                
                print(kolcsonzo.berelheto_autok_listaz(datum))
            
            elif valasztas == "3":
                print("\n" + kolcsonzo.autok_listaz())
                rendszam = input("\nAdja meg a kívánt autó rendszámát: ").strip().upper()
                
                while True:
                    datum_str = input("Adja meg a bérlés dátumát (ÉÉÉÉ-HH-NN): ").strip()
                    try:
                        datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
                        if datum < datetime.now().date():
                            print("Hiba: A dátum múltbeli! Adjon meg jövőbeli dátumot.")
                        else:
                            break
                    except ValueError:
                        print("Hiba: Érvénytelen dátum formátum! Használja az ÉÉÉÉ-HH-NN formátumot.")
                
                siker, uzenet = kolcsonzo.berel(rendszam, datum)
                print("\n" + uzenet)
            
            elif valasztas == "4":
                berlesek = kolcsonzo.get_berlesek()
                if not berlesek:
                    print("\nNincsenek aktív bérlések.")
                    continue
                
                print("\nAktív bérlések:")
                for i, berles in enumerate(berlesek, 1):
                    print(f"{i}. Rendszám: {berles.auto.rendszam}, Dátum: {berles.datum.strftime('%Y-%m-%d')}")
                
                try:
                    sorszam = int(input("\nAdja meg a lemondani kívánt bérlés sorszámát: ")) - 1
                    if 0 <= sorszam < len(berlesek):
                        berles = berlesek[sorszam]
                        siker, uzenet = kolcsonzo.lemond(berles.auto.rendszam, berles.datum)
                        print("\n" + uzenet)
                    else:
                        print("Hiba: Érvénytelen sorszám!")
                except ValueError:
                    print("Hiba: Számot adjon meg!")
            
            elif valasztas == "5":
                print("\n" + kolcsonzo.berlesek_listaz())
            
            elif valasztas == "6":
                print("\nKilépés...")
                break
            
            else:
                print("\nHiba: Érvénytelen választás!")
        
        except KeyboardInterrupt:
            print("\n\nKilépés...")
            break
        except Exception as e:
            print(f"\nHiba történt: {e}")

if __name__ == "__main__":
    felhasznaloi_interfesz()