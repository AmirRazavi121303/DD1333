import random

class Kort():
    def __init__(self, färg, symbol, fyllnadsgrad, n_symboler):
        self.färg: str = färg
        self.symbol: str = symbol
        self.fyllnadsgrad: int = fyllnadsgrad
        self.n_symboler: int = n_symboler
        
        self.visas = False
    
    def vänd(self):
        self.visas = not self.visas
    
    def __str__(self):
        if self.visas:
            return f"{self.färg}, {self.symbol}, {self.fyllnadsgrad}, {self.n_symboler}"
        else:
            return "Baksida"

class Kortlek():
    def __init__(self):
        self.kort = []
        self.generera_kort()

    def generera_kort(self):
        färg = ["red", "green", "blue"]
        symbol = ["Γ", "Π", "Δ"] 
        fyllnadsgrad = [10, 20, 30]
        antal_symboler = [1, 2, 3]
        
        for f in färg:
            for s in symbol:
                for g in fyllnadsgrad:
                    for n in antal_symboler:
                        self.kort.append(Kort(f, s, g, n))

    def blanda(self):
        random.shuffle(self.kort)

    def dra_kort(self): #plockar det högsta kortet i leken
        draget_kort = self.kort.pop()
        draget_kort.vänd()
        return draget_kort

    def antal_kvar(self):
        return len(self.kort)

class Spelbord():
    def __init__(self, kortlek):
        self.bordets_kort = []
        self.fyll_på_bordet(kortlek)
    
    def fyll_på_bordet(self, kortlek):
        while len(self.bordets_kort) < 6 and kortlek.antal_kvar() > 0:
            kort = kortlek.dra_kort()
            self.bordets_kort.append(kort)
    
    def välj_kort(self, kortlek):
        a = 6
        self.valda_kort = []
        self.valda_index = [i for i in range(1,a+1)]
        
        while len(self.valda_index) > 3:
            try:
                user_input = int(input(f"Välj ett kort (1-{a}) ({len(self.valda_kort) + 1} / {a//2})"))
                if user_input in self.valda_index:
                    self.valda_index.remove(user_input)
                    self.valda_kort.append(self.bordets_kort[user_input-1])
                
                elif user_input > a:
                    print("Det finns inte så många kort i leken")
                else:
                    print("Det kortet har du redan valt, försök igen")
            except Exception:
                print("Ogiltigt svar, försök igen")
        return self.valda_kort
    
    def ersätt_valda_kort(self, kortlek: Kortlek):
        for i in range(1,7): #tänk på detta om a skulle förändras
            if i not in self.valda_index and kortlek.antal_kvar() > 0:
                nytt_kort = kortlek.dra_kort()
                if not nytt_kort.visas:
                    nytt_kort.vänd()
                self.bordets_kort[i-1] = nytt_kort

    def räkna_poäng(self):
        poäng = 0
        k1, k2, k3 = self.valda_kort[0], self.valda_kort[1], self.valda_kort[2]
        färger_set = {k1.färg, k2.färg, k3.färg}
        symboler_set = {k1.symbol, k2.symbol, k3.symbol}
        fyllnadsgrader_set = {k1.fyllnadsgrad, k2.fyllnadsgrad, k3.fyllnadsgrad}
        antal_symboler_set = {k1.n_symboler, k2.n_symboler, k3.n_symboler}
        
        egenskaper = [färger_set, symboler_set, fyllnadsgrader_set, antal_symboler_set]
        
        giltig_trippel = False
        inget_lika = True
        
        for e in egenskaper:
            if len(e) == 1:
                giltig_trippel = True
                inget_lika = False
                break
            elif len(e) == 2:
                inget_lika = False
        
        if inget_lika and not giltig_trippel:
            poäng = poäng +3
        elif giltig_trippel:
            poäng = poäng +2
        else:
            poäng = poäng -1
        
        return poäng
    
    def fortsätt(self):
        if input("Vill du fortsätta spelet (y/n)?").lower() == "y":
            return True
        else:
            return False

def main():
        kortlek = Kortlek()
        kortlek.blanda()
        
        bord = Spelbord(kortlek)
        bord.fyll_på_bordet(kortlek)
        
        total_poäng = 0
        
        while kortlek.antal_kvar() > 0:
            print(f"Antalet kort kvar i leken: {kortlek.antal_kvar()}")
            
            valda_kort = bord.välj_kort(kortlek)
            
            print("Dina kort är:")
            for kort in valda_kort:
                print(kort)
            
            omgång_poäng = bord.räkna_poäng()
            total_poäng += omgång_poäng
            
            print(f"Utdelad poäng denna runda: {omgång_poäng}")
            print(f"Total poäng: {total_poäng}")
            
            bord.ersätt_valda_kort(kortlek)
            if not bord.fortsätt():
                break
        print(f"Spelet är slut, du fick {total_poäng} poäng!")

if __name__ == "__main__":
    main()