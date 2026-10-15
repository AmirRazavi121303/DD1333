import random
import tkinter as tk
from tkinter import messagebox
import itertools
class Kort():#initierar varje kort. klassen används för att spaka kortleken
    def __init__(self, färg, symbol, fyllnadsgrad, n_symboler):
        self.färg: str = färg
        self.symbol: str = symbol
        self.fyllnadsgrad: int = fyllnadsgrad
        self.n_symboler: int = n_symboler
        
        self.visas = False
    
    def vänd(self): #vänder på kortet, onödigt nu men kan va användbart vid utveckling av nya funktioner
        self.visas = not self.visas
    
    def __str__(self): #sträng funktion för när man skriver ut varje kort
        if self.visas:
            return f"{self.färg}, {self.symbol}, {self.fyllnadsgrad}, {self.n_symboler}"
        else:
            return "Baksida"
class Kortlek(): #skapar varje kort i kortleken, med funktion att dra och blanda och räkna antalet kvar
    def __init__(self):
        self.kort = []
        self.generera_kort()

    def generera_kort(self): #genererar korten i kortleken
        färg = ["red", "green", "blue"]
        symbol = ["Γ", "Π", "Δ"] 
        fyllnadsgrad = [10, 20, 30]
        antal_symboler = [1, 2, 3]
        
        for f in färg:
            for s in symbol:
                for g in fyllnadsgrad:
                    for n in antal_symboler:
                        self.kort.append(Kort(f, s, g, n))

    def blanda(self): #blandar slumpmässigt
        random.shuffle(self.kort)

    def dra_kort(self): #plockar det högsta kortet i leken
        draget_kort = self.kort.pop()
        draget_kort.vänd()
        return draget_kort

    def antal_kvar(self): #räknar antal kort kvar
        return len(self.kort)
class Spelbord(): #huvudklassen, här kan man fylla på bordet, plocka kort, ersätta de valda, räkna poängen i en hand och fråga spelaren om de vill fortsätta
    #vi har också en bot som löser bästa möjliga patiens
    def __init__(self, kortlek):
        self.bordets_kort = []
        self.valda_index = []
        self.valda_kort = []
        self.sparad_sekvens = []
        self.antal_kort_på_bordet = 6
        self.antal_kort_i_handen = 3
        self.fyll_på_bordet(kortlek)
    
    def fyll_på_bordet(self, kortlek): #fyller på bordet vid spelets start, används inte för hela rundan efter det
        a = self.antal_kort_på_bordet
        while len(self.bordets_kort) < a and kortlek.antal_kvar() > 0:
            kort = kortlek.dra_kort()
            self.bordets_kort.append(kort)
    
    def välj_kort(self, kortlek, bot_check): #funktionen för o plocka kort från leken, beroende på om användaren är människa eller bot
        self.valda_kort.clear()
        self.valda_index.clear()
        while len(self.valda_index) < self.antal_kort_i_handen:
        
            try:
                if not bot_check:
                    user_input = int(input(f"Välj ett kort (1-{self.antal_kort_på_bordet}) ({len(self.valda_kort) + 1} / {self.antal_kort_på_bordet//2})"))
                    if user_input > self.antal_kort_på_bordet:
                        print("Det finns inte så många kort i leken")
                    elif (user_input - 1) not in self.valda_index:
                        self.valda_index.append(user_input-1)
                        self.valda_kort.append(self.bordets_kort[user_input-1])
                    else:
                        print("Det kortet har du redan valt, försök igen")
                else:
                    self.valda_kort = self.greedy_bot()
            except Exception:
                print("Ogiltigt svar, försök igen")
        self.sparad_sekvens.append(self.valda_kort)
        return self.valda_kort
    
    #
    def ersätt_valda_kort(self, kortlek): #byter ut de tomma platserna på bordet med översta kortet i leken
        for i in range(0, self.antal_kort_på_bordet): #tänk på detta om a skulle förändras
            if i in self.valda_index:
                if kortlek.antal_kvar() > 0:
                    self.bordets_kort[i] = kortlek.dra_kort()
                else:
                    self.bordets_kort[i] = None
    
    def greedy_bot(self): #för varje tillgängliga hand av trippletter tar det denhanden som ger mest poäng
        giltiga_index = []
        
        for i, kort in enumerate(self.bordets_kort):
            if kort is not None:
                giltiga_index.append(i)
        
        if len(giltiga_index) < self.antal_kort_i_handen:
            return []
        
        max_poäng = -100
        bästa_kombination_index = []
        
        for kombination in itertools.combinations(giltiga_index, self.antal_kort_i_handen):
            self.valda_kort.clear()
            for i in kombination:
                self.valda_kort.append(self.bordets_kort[i])
            poäng = self.räkna_poäng()
            
            if poäng > max_poäng:
                max_poäng = poäng
                bästa_kombination_index = list(kombination)
        self.valda_index = bästa_kombination_index
        self.valda_kort.clear()
        for i in self.valda_index:
            self.valda_kort.append(self.bordets_kort[i])
        return self.valda_kort
    
    def räkna_poäng(self): #räknar poängen för en hand
        poäng = 0
        färger_set = set()
        symboler_set = set()
        fyllnadsgrader_set = set()
        antal_symboler_set = set()
        for kort in self.valda_kort:
            färger_set.add(kort.färg)
            symboler_set.add(kort.symbol)
            fyllnadsgrader_set.add(kort.fyllnadsgrad)
            antal_symboler_set.add(kort.n_symboler)
        
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
    
    def fortsätt(self, bot_check): #frågar om användaren vill fortsätta
        if not bot_check:
            if input("Vill du fortsätta spelet (y/n)?").lower() == "y":
                return True
            else:
                return False
        else:
            return True

def MonteCarloSim(): #itererar spelet om och om igen för att hitta största möjliga poängsumma, följer lagen om stora tal
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
    for runda in högsta_sekvens:
        print(f"-----runda {högsta_sekvens.index(runda)+1} ------")
        for kort in runda:
            print(kort)
    print(f"det högsta poänget jag lyckades få var {högsta_poäng}")

def main(bot_check): #här körs hela leken, alla funktioner och klasser anropas här
    kortlek = Kortlek()
    kortlek.blanda()
    
    bord = Spelbord(kortlek)
    bord.fyll_på_bordet(kortlek)
    
    total_poäng = 0
    sekvens = []
    
    antal = 6
    
    while antal >=3 or kortlek.antal_kvar() > 0:
        
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
        for k in bord.bordets_kort:
            if k is None:
                antal -= 1
        if not bord.fortsätt(bot_check):
            break
    if not bot_check:
        print(f"Spelet är slut, du fick {total_poäng} poäng!")
    else:
        return total_poäng, sekvens

if __name__ == "__main__": #huvudprogrammet
    print("--- VÄLKOMMEN TILL PATIENS MED 81 KORT ---")
    while True:
        val = int(input("Vill du: \n[1] Spela själv,\n[2] Låta datorn lösa patiensen med monte carlo,\n[3] avsluta\n"))
        
        if val == 1:
            main(False)
        elif val == 2:
            MonteCarloSim()
            
        else:
            break
