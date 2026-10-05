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
        self.track_count: int = track_count 
        
        #4 Trädrelationer
        self.parent = None
        self.children = []

def parsing(folder_path):
    projects = [] 
    for filename in os.listdir(folder_path):
        if filename.endswith(".flp") and not filename.startswith('.'):
            filepath = os.path.join(folder_path, filename)
            try:
                flp = pyflp.parse(filepath)
                name = str(filename).replace('.flp', '').lower()
                add_hashes = hashes(flp)
                name_words, plugins = find_name_words(flp)
                
                tempo = getattr(flp, "tempo", 100.0)
                project = Project(filepath, name, tempo, len(flp.channels)) #avvakta med len(flp.channels) för nu
                
                project.hash = add_hashes
                
                project.name_words = name_words
                project.name_words.add(name)
                
                project.plugins = plugins
                
                projects.append(project)
            except Exception as e:
                print(f"Couldn't read the file {filename}: {e} ")
    return projects

def hashes(flp):
    add_hashes = set()
    for channel in flp.channels:
        if hasattr(channel, "sample_path") and channel.sample_path:
            md5hash = signature(channel)
            if md5hash:
                add_hashes.add(md5hash)
    return add_hashes

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
            return None #?vad händer i parsing om det blir exception?
    
    return None #om sample path skulle vara tom så kommer detta att behövas

def find_name_words(flp):
    name_words = set()
    plugins = set()
    for channel in flp.channels:
        if channel.name:
            name_words.add(channel.name.replace(" ","").lower())
        if hasattr(channel, 'plugin') and channel.plugin:
            plugins.add(channel.plugin.name)
    return name_words, plugins

def find_similar(flp, A, B):
    for word in A.name_words:
        if A in B:
            pass

def main(folder_path):
    mapp = parsing(folder_path)
    print(f"-----{mapp[0].filename}----- \n {len(mapp[0].hash)} hashar \n, ord: {mapp[0].name_words},\n plugins: {mapp[0].plugins}")
    print(f"-----{mapp[1].filename}----- \n {len(mapp[1].hash)} hashar \n, ord: {mapp[1].name_words} ,\n plugins: {mapp[1].plugins}")
    print('-----------')
    print(f"de hashen som är likadana är {mapp[0].hash.intersection(mapp[1].hash)}")

if __name__ == "__main__":
    main('/Users/amir/Downloads/CodeAmir/DD1333/test')

"""
hur kan man lättast avgöra om ett projekt är förälder till ett annat?
1. om ena av projekten innehåller en fil som har samma namn som 
"""