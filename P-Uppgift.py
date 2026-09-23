import pyflp
import os
import hashlib

class Project():
    def __init__(self, filepath, filename, tempo, track_count):
        #1 identification
        self.filepath: str = filepath
        self.filename: str = filename
        self.mod_time: float = os.path.getmtime(filepath)
        
        #2 Minhash
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
                
                add_hashes = set()
                for channel in flp.channels:
                    if hasattr(channel, "sample_path") and channel.sample_path:
                        md5hash = signature(channel)
                        if md5hash:
                            add_hashes.add(md5hash)
                
                tempo = getattr(flp, "tempo", 100.0)
                project = Project(filepath, filename, tempo, len(flp.channels)) #avvakta med len(flp.channels) för nu
                project.hash = add_hashes
                
                projects.append(project)
            except Exception as e:
                print(f"Couldn't read the file {filename}: {e} ")
    
    return projects

def signature(channel):
    full_sample_path = str(channel.sample_path)
    try: #om den sökvägen finns på datorn
        with open(full_sample_path, "rb") as f: #läser in samplet som binär fil
            md5 = hashlib.md5()
            sample = f.read()
            md5.update(sample)
            return md5.hexdigest()
        
    except Exception: 
        #Fallback om det ej skulle gå att läsa in samplet så tittar den bara på namnet på den istället
        if full_sample_path:
            return full_sample_path #vad händer i parsing om det blir exception
    
    return None #om sample path skulle vara tom så kommer detta att behövas

"""
project_lineage/
│
├── main.py              # Huvudfilen som kör hela pipelinen (Steg 1 -> 2 -> 3 -> 4)
├── models.py            # Dataklasser: Project och Relation
├── step1_signature.py   # Bygger projektets signatur (hashar + ord)
├── step2_candidates.py  # Hittar kandidatpar (MinHash / Inverted Index)
├── step3_direction.py   # Beräknar sannolikhet/kostnad för vem som är förälder
└── step4_tree.py        # Bygger trädet och genererar utdatan/rapporten"""