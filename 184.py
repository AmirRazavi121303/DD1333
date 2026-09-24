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
        if not self.visas:
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
        return draget_kort

    def antal_kvar(self):
        return len(self.kort)

class Spelbord():
    #hanterar de 6 kort från "dealern" och 3 till spelaren
    def __init__(self, kortlek):
        self.bordets_kort = []
        self.placera_kort(kortlek)
    
    def placera_kort(self, kortlek):
        while len(self.bordets_kort) < 6:
            self.bordets_kort.append(kortlek.dra_kort())
    
    def välj_kort(self, kortlek):
        self.valda_kort = []
        self.valda_index = [1, 2, 3, 4, 5, 6]
        
        while len(self.valda_index) > 3:
            try:
                user_input = int(input(f"Välj ett kort, ange numret ovanför kortet. ({len(self.valda_kort) + 1} / 3)"))
                if user_input in self.valda_index:
                    self.valda_index.remove(user_input)
                    self.valda_kort.append(self.bordets_kort[user_input-1])
                
                else:
                    print("Det kortet har du redan valt, försök igen")
            except Exception:
                print("Ogiltigt svar, försök igen")
        
        for i in range(1,7):
            if i not in self.valda_index:
                self.bordets_kort[i-1] = kortlek.dra_kort()
        return self.valda_kort

    def räkna_poäng(self):
        poäng = 0
        card1 = set(self.valda_kort[0])
        card2 = set(self.valda_kort[1])
        card3 = set(self.valda_kort[2])
        
        if (card1.intersection(card2)).intersection(card3):
            poäng = poäng + 2
        elif not (card1.intersection(card2) and card1.union(card2).intersection(card3)):
            poäng = poäng + 3
        else:
            poäng = poäng -1
        return poäng
    
    def __str__(self):
        if self.visas:
            return f"{self.färg}, {self.symbol}, {self.fyllnadsgrad}, {self.n_symboler}"
        else:
            return "Baksida"



min_kortlek = Kortlek()
min_kortlek.blanda()
mitt_bord = Spelbord(min_kortlek)
mina_kort = mitt_bord.välj_kort(min_kortlek)
poäng = mina_kort.räkna_poäng()
print(f"första kortet är [{mina_kort[0]}] andra kortet är [{mina_kort[1]}] tredje kortet är [{mina_kort[2]}]")
print(f"dina poäng är {poäng}")
