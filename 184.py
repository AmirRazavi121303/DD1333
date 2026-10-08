import random
import itertools
import copy

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
        self.valda_index = []
        self.valda_kort = []
        self.sparad_sekvens = []
        self.fyll_på_bordet(kortlek)
    
    def fyll_på_bordet(self, kortlek):
        while len(self.bordets_kort) < 6 and kortlek.antal_kvar() > 0:
            kort = kortlek.dra_kort()
            self.bordets_kort.append(kort)
    
    def välj_kort(self, kortlek, bot_check):
        a = 6
        self.valda_kort.clear()
        self.valda_index.clear()
        while len(self.valda_index) < 3:
        
            try:
                if not bot_check:
                    user_input = int(input(f"Välj ett kort (1-{a}) ({len(self.valda_kort) + 1} / {a//2})"))
                    if user_input > a:
                        print("Det finns inte så många kort i leken")
                    elif (user_input - 1) not in self.valda_index:
                        self.valda_index.append(user_input-1)
                        self.valda_kort.append(self.bordets_kort[user_input-1])
                    else:
                        print("Det kortet har du redan valt, försök igen")
                else:
                    bot_input = random.randint(1,6)
                    if (bot_input - 1) not in self.valda_index:
                        self.valda_index.append(bot_input-1)
                        self.valda_kort.append(self.bordets_kort[bot_input-1])
            except Exception:
                print("Ogiltigt svar, försök igen")
        self.sparad_sekvens.append(self.valda_kort)
        return self.valda_kort
    
    def ersätt_valda_kort(self, kortlek: Kortlek):
        for i in range(0,6): #tänk på detta om a skulle förändras
            if i in self.valda_index:
                if kortlek.antal_kvar() > 0:
                    self.bordets_kort[i] = kortlek.dra_kort()
                else:
                    self.bordets_kort[i] = None
    
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
    
    def fortsätt(self, bot_check):
        if not bot_check:
            if input("Vill du fortsätta spelet (y/n)?").lower() == "y":
                return True
            else:
                return False
        else:
            return True

class Patienslösare():
    def __init__(self, start_bord, start_kortlek):
        self.start_bord = start_bord
        self.start_kortlek = start_kortlek
    
    def sök_bästa_sekvens(self, bord, kortlek):
        giltiga_index = [i for i, kort in enumerate(bord.bordets_kort) if kort is not None]
        
        #skapar alla unika 3 kortskombinationer från indexen
        alla_tripplar = list(itertools.combinations(giltiga_index, 3))
        
        #Basfall: om inga 3 kort finss kvar slutar spelet
        if not alla_tripplar or len(giltiga_index) < 3:
            return 0, []
        
        bästa_poäng = float('-inf')
        bästa_sekvens = []
        
        for kombination in alla_tripplar:
            #vi ska skapa kopior av bordet och leken för att testa dragen
            sim_bord = copy.deepcopy(bord)
            sim_kortlek = copy.deepcopy(kortlek)
            
            #bordets_kort är en metod från Kort() som dyker upp här med. 
            sim_bord.valda_index = list(i +1 for i in list(kombination))
            sim_bord.valda_kort = [sim_bord.bordets_kort[i] for i in kombination]
            
            drag_poäng = sim_bord.räkna_poäng()
            
            #vi bryr oss inte ens om ett drag är -1p, jätte viktigt stycke
            if drag_poäng < 0 and len(alla_tripplar) > 1:
                continue
            
            #fyll på det simulerade bordet med 3 simulerade kort
            sim_bord.ersätt_valda_kort(sim_kortlek)
            
            #rekursiv anrop, den utför funktionen igen för o se hur många poäng man kan få från en given position
            framtida_poäng, framtida_sekvens = self.sök_bästa_sekvens(sim_bord, sim_kortlek)
            
            #allt härifrån ner händer först efter att alla möjliga blandningar har undersökts
            totalt_för_denna_väg = drag_poäng + framtida_poäng
            
            if totalt_för_denna_väg > bästa_poäng:
                bästa_poäng = totalt_för_denna_väg
                
                bästa_sekvens = [(sim_bord.valda_kort, drag_poäng)] + framtida_sekvens
        return bästa_poäng, bästa_sekvens

def MonteCarloSim():
    count = 0
    högsta_poäng = 0
    högsta_sekvens = list()
    M = 10000
    while count < M:
        omgångens_poäng, omgångens_sekvens = main(True)
        if omgångens_poäng > högsta_poäng:
            högsta_poäng = omgångens_poäng
            högsta_sekvens = omgångens_sekvens
        count +=1
        if count % (M/10) == 0:
            print(f'omgång {count} klar')
    #bästa_omgång = max(poäng for poäng in omgångar.values())
    for runda in högsta_sekvens:
        print(f"-----runda {högsta_sekvens.index(runda)+1} ------")
        for kort in runda:
            print(kort)
    print(f"det högsta poänget jag lyckades få var {högsta_poäng}")


def main(bot_check):
    kortlek = Kortlek()
    kortlek.blanda()
    
    bord = Spelbord(kortlek)
    bord.fyll_på_bordet(kortlek)
    
    total_poäng = 0
    sekvens = []
    
    while kortlek.antal_kvar() > 0:
        if not bot_check:
            print(f"Antalet kort kvar i leken: {kortlek.antal_kvar()}")
            for kort in bord.bordets_kort:
                print(f"kort {bord.bordets_kort.index(kort)+1}: {kort}")
            
            valda_kort = bord.välj_kort(kortlek, bot_check)
            
            print("Dina kort är:")
            for kort in valda_kort:
                print(kort)
            
            omgång_poäng = bord.räkna_poäng()
            total_poäng += omgång_poäng
            
            print(f"Utdelad poäng denna runda: {omgång_poäng}")
            print(f"Total poäng: {total_poäng}")
            
            bord.ersätt_valda_kort(kortlek)
        else:
            valda_kort = bord.välj_kort(kortlek, bot_check)
            
            sekvens.append(valda_kort.copy())
            
            omgång_poäng = bord.räkna_poäng()
            total_poäng += omgång_poäng
            
            bord.ersätt_valda_kort(kortlek)
        if not bord.fortsätt(bot_check):
            break
    if not bot_check:
        print(f"Spelet är slut, du fick {total_poäng} poäng!")
    if bot_check:
        return total_poäng, sekvens

if __name__ == "__main__":
    print("--- VÄLKOMMEN TILL PATIENS MED 81 KORT ---")
    while True:
        val = int(input("Vill du: \n[1] Spela själv,\n[2] Låta datorn lösa patiensen med monte carlo,\n[3] avsluta? "))
        
        if val == 1:
            main(False)
        elif val == 2:
            MonteCarloSim()
            
        else:
            break