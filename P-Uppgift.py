import pyflp
import os

class Project():
    def __init__(self, filepath, filename, tempo, track_count):
        #1 identification
        self.filepath: str = filepath
        self.filename: str = filename
        self.mod_time: float = os.path.getmtime(filepath)
        
        #2 Signatur
        self.hash: set[str] = set()
        self.name_words: set[str] = set()
        self.plugins: set[str] = set()
        
        #3 Projektdetaljer
        self.tempo: float = tempo
        self.track_count: int = track_count #nya spår har fler kanaler än sina föräldrar
        
        #4 Trädrelationer
        self.parent = None
        self.children = []

def parsing(folder_path):
    projects = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".flp"):
            filepath = os.path.join(folder_path, filename)
            try:
                flp = pyflp.parse(filepath)
                
                tempo = getattr(flp, "tempo", 100.0)
                project = Project(filepath, filename, flp.tempo, len(flp.channels)) #avvakta med len(flp.channels) för nu
                
                projects.append(project)
            except Exception as e:
                print(f"Kunde inte läsa filen {filename}: {e} ")

def signature(flp, filename):
    
    return

"""
project_lineage/
│
├── main.py              # Huvudfilen som kör hela pipelinen (Steg 1 -> 2 -> 3 -> 4)
├── models.py            # Dataklasser: Project och Relation
├── step1_signature.py   # Bygger projektets signatur (hashar + ord)
├── step2_candidates.py  # Hittar kandidatpar (MinHash / Inverted Index)
├── step3_direction.py   # Beräknar sannolikhet/kostnad för vem som är förälder
└── step4_tree.py        # Bygger trädet och genererar utdatan/rapporten"""