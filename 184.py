import random
import tkinter as tk
from tkinter import messagebox
import itertools
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
        self.antal_kort_på_bordet = 6
        self.antal_kort_i_handen = 3
        self.fyll_på_bordet(kortlek)
    
    def fyll_på_bordet(self, kortlek):
        a = self.antal_kort_på_bordet
        while len(self.bordets_kort) < a and kortlek.antal_kvar() > 0:
            kort = kortlek.dra_kort()
            self.bordets_kort.append(kort)
    
    def välj_kort(self, kortlek, bot_check):
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
    
    def ersätt_valda_kort(self, kortlek: Kortlek):
        for i in range(0, self.antal_kort_på_bordet): #tänk på detta om a skulle förändras
            if i in self.valda_index:
                if kortlek.antal_kvar() > 0:
                    self.bordets_kort[i] = kortlek.dra_kort()
                else:
                    self.bordets_kort[i] = None
    
    def greedy_bot(self):
        giltiga_index = [
            i for i, kort in enumerate(self.bordets_kort) if kort is not None
        ]
        if len(giltiga_index) < self.antal_kort_i_handen:
            return []
        
        max_poäng = -100
        bästa_kombination_index = []
        
        for kombination in itertools.combinations(giltiga_index, self.antal_kort_i_handen):
            self.valda_kort = [self.bordets_kort[i] for i in kombination]
            poäng = self.räkna_poäng()
            
            if poäng > max_poäng:
                max_poäng = poäng
                bästa_kombination_index = list(kombination)
        self.valda_index = bästa_kombination_index
        self.valda_kort = [self.bordets_kort[i] for i in self.valda_index]
        return self.valda_kort
    
    def räkna_poäng(self):
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
    
    def fortsätt(self, bot_check):
        if not bot_check:
            if input("Vill du fortsätta spelet (y/n)?").lower() == "y":
                return True
            else:
                return False
        else:
            return True

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
    
    while kortlek.antal_kvar() > 0 or any(k is not None for k in bord.bordets_kort):
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
        val = int(input("Vill du: \n[1] Spela själv,\n[2] Låta datorn lösa patiensen med monte carlo,\n[3] avsluta\n"))
        
        if val == 1:
            main(False)
        elif val == 2:
            MonteCarloSim()
            
        else:
            break

class GUI:
    def __init__(self):
        
        self.kortlek = Kortlek()
        self.kortlek.blanda()

        
        self.bord = Spelbord(self.kortlek)

        
        self.valda = []

        self.total_poäng = 0

        
        self.fönster = tk.Tk()
        self.fönster.title("Patiens")
        self.fönster.geometry("850x400")

        # Text högst upp i fönstret
        self.info = tk.Label(
            self.fönster,
            text="Klicka på tre kort",
            font=("Arial", 14)
        )
        self.info.pack(pady=10)

        # Visar poäng och antal kort kvar i leken
        self.poäng_text = tk.Label(
            self.fönster,
            text="Poäng: 0"
        )
        self.poäng_text.pack()

        # En ruta som innehåller alla sex kortknappar
        self.ram = tk.Frame(self.fönster)
        self.ram.pack(pady=20)

        # Skapar sex knappar, en för varje kortplats
        self.knappar = []

        for i in range(6):
            knapp = tk.Button(
                self.ram,
                text="",
                width=15,
                height=5,
                command=lambda index=i: self.klicka_kort(index)
            )

            # Placerar knappen bredvid de andra knapparna
            knapp.grid(row=0, column=i, padx=4)

            # Sparar knappen så att vi kan ändra den senare
            self.knappar.append(knapp)

        # Knapp som räknar poäng och byter ut valda kort
        self.spela_knapp = tk.Button(
            self.fönster,
            text="Räkna poäng och byt kort",
            command=self.spela_runda
        )
        self.spela_knapp.pack(pady=10)

        # Visar korten första gången
        self.uppdatera_kort()

        # Startar GUI:t
        self.fönster.mainloop()

    def klicka_kort(self, index):
        # Hämtar kortet på den klickade platsen
        kort = self.bord.bordets_kort[index]

        # Gör inget om platsen är tom
        if kort is None:
            return

        # Om kortet redan är valt avmarkerar vi det
        if index in self.valda:
            self.valda.remove(index)

        # Annars väljer vi kortet om färre än tre är valda
        elif len(self.valda) < 3:
            self.valda.append(index)

        # Uppdaterar knapparnas färger och text
        self.uppdatera_kort()

    def uppdatera_kort(self):
        # Går igenom alla sex kortplatser
        for i in range(6):
            kort = self.bord.bordets_kort[i]
            knapp = self.knappar[i]

            # Om det finns ett kort på platsen
            if kort is not None:
                # Visar kortets egenskaper
                text = (
                    f"Färg: {kort.färg}\n"
                    f"Symbol: {kort.symbol}\n"
                    f"Fyllnad: {kort.fyllnadsgrad}\n"
                    f"Antal: {kort.n_symboler}"
                )

                knapp.config(text=text, state="normal")

                # Gult betyder att kortet är valt
                if i in self.valda:
                    knapp.config(bg="yellow")
                else:
                    knapp.config(bg="white")

            else:
                # Visar en tom plats när inget kort finns kvar
                knapp.config(
                    text="Tom plats",
                    bg="lightgray",
                    state="disabled"
                )

        # Visar poäng och antal kort kvar
        self.poäng_text.config(
            text=f"Poäng: {self.total_poäng} | "
                    f"Kort kvar i leken: {self.kortlek.antal_kvar()}"
        )

        # Visar hur många kort som är valda
        self.info.config(
            text=f"Du har valt {len(self.valda)} av 3 kort"
        )

    def spela_runda(self):
        # Spelaren måste välja exakt tre kort
        if len(self.valda) != 3:
            messagebox.showinfo(
                "Välj kort",
                "Du måste välja exakt tre kort!"
            )
            return

        # Sparar de valda kortens index i det befintliga spelbordet
        self.bord.valda_index = self.valda.copy()

        # Sparar själva korten i samma ordning
        self.bord.valda_kort = [
            self.bord.bordets_kort[i] for i in self.valda
        ]

        # Använder din befintliga funktion för poängräkning
        poäng = self.bord.räkna_poäng()

        # Lägger till rundans poäng
        self.total_poäng += poäng

        # Använder din befintliga funktion för att byta kort
        self.bord.ersätt_valda_kort(self.kortlek)

        # Nollställer valet inför nästa runda
        self.valda.clear()

        # Uppdaterar korten och poängen på skärmen
        self.uppdatera_kort()

        # Visar rundans resultat
        messagebox.showinfo(
            "Resultat",
            f"Du fick {poäng} poäng denna runda!\n"
            f"Total poäng: {self.total_poäng}"
        )

        # Kontrollerar om minst tre kort finns kvar på bordet
        antal_kort = sum(
            1 for kort in self.bord.bordets_kort
            if kort is not None
        )

        if antal_kort < 3:
            self.info.config(
                text="Spelet är slut! Du fick "
                        f"{self.total_poäng} poäng."
            )
            self.spela_knapp.config(state="disabled")
