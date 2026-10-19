
import importlib.util

# Läser in ditt befintliga program utan att starta terminalmenyn
spec = importlib.util.spec_from_file_location(
    "patiens_program", "184.py"
)

program = importlib.util.module_from_spec(spec)
spec.loader.exec_module(program)

# Startar GUI-klassen som ligger i 184.py
program.GUI()

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
        #text högst upp i fönstret
        self.info = tk.Label(
            self.fönster,
            text="Klicka på tre kort",
            font=("Arial", 14)
        )
        self.info.pack(pady=10)
        #visar poäng och antal kort kvar i leken
        self.poäng_text = tk.Label(
            self.fönster,
            text="Poäng: 0"
        )
        self.poäng_text.pack(pady=20)
        #en ruta som innehåller alla sex kortknappar
        self.ram = tk.Frame(self.fönster)
        self.ram.pack(pady=20)
        #skapar sex knappar, en för varje kortplats
        self.knappar = []
        for i in range(6):
            knapp = tk.Button(
                self.ram,
                text="",
                width=15,
                height=5,
                command=lambda index=i: self.klicka_kort(index)
            )
            #placerar knappen bredvid de andra knapparna
            knapp.grid(row=0, column=i, padx=4)
            #sparar knappen så att vi kan ändra den senare
            self.knappar.append(knapp)
        #knapp som räknar poäng och byter ut valda kort
        self.spela_knapp = tk.Button(
            self.fönster,
            text="Räkna poäng och byt kort",
            command=self.spela_runda
        )
        self.spela_knapp.pack(pady=10)
        #visar korten första gången
        self.uppdatera_kort()
        #startar GUI:t, all gui måste komma innan dehär
        self.fönster.mainloop()
    def klicka_kort(self, index):
        kort = self.bord.bordets_kort[index]
        if kort is None:
            return
        if index in self.valda:
            self.valda.remove(index)
        elif len(self.valda) < 3:
            self.valda.append(index)
        self.uppdatera_kort()
    def uppdatera_kort(self):
        for i in range(6):
            kort = self.bord.bordets_kort[i]
            knapp = self.knappar[i]
            if kort is not None:
                text = (
                    f"Färg: {kort.färg}\n"
                    f"Symbol: {kort.symbol}\n"
                    f"Fyllnad: {kort.fyllnadsgrad}\n"
                    f"Antal: {kort.n_symboler}"
                )
                knapp.config(text=text, state="normal")
                # gult betyder att kortet är valt
                if i in self.valda:
                    knapp.config(bg="yellow")
                else:
                    knapp.config(bg="white")
            else:
                knapp.config(
                    text="Tom plats",
                    bg="lightgray",
                    state="disabled"
                )
        self.poäng_text.config(
            text=f"Poäng: {self.total_poäng} | "
                    f"Kort kvar i leken: {self.kortlek.antal_kvar()}"
        )
        #visar hur många kort som är valda
        self.info.config(
            text=f"Du har valt {len(self.valda)} av 3 kort"
        )
    def spela_runda(self):
        
        if len(self.valda) != 3:
            messagebox.showinfo(
                "Välj kort",
                "Du måste välja exakt tre kort!"
            )
            return
        self.bord.valda_index = self.valda.copy()
        for i in self.valda:
            self.bord.valda_kort.append(self.bord.bordets_kort[i])
        # använder befintliga funktionen för main
        poäng = self.bord.räkna_poäng()
        self.total_poäng += poäng
        self.bord.ersätt_valda_kort(self.kortlek)
        self.valda.clear()
        self.uppdatera_kort()
        
        #visar rundans resultat
        messagebox.showinfo(
            "Resultat",
            f"Du fick {poäng} poäng denna runda!\n"
            f"Total poäng: {self.total_poäng}"
        )
        for kort in self.bord.bordets_kort:
            if kort is not None:
                antal_kort +=1
        if antal_kort < 3:
            self.info.config(
                text="Spelet är slut! Du fick "
                        f"{self.total_poäng} poäng."
            )
            self.spela_knapp.config(state="disabled")

