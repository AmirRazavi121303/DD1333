import pyflp
import os
import hashlib
class Project():
    def __init__(self, filepath, filename, tempo, track_count):
        #1 identification
        self.filepath: str = filepath
        self.filename: str = filename
        self.m_time: float = os.path.getmtime(filepath)
        self.c_time: float = os.path.getctime(filepath)
        
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

def find_similar(A, B):
    def checker(A, B):
        set_same = set()
        poäng = 0
        poäng +=1
        if A.filename.replace(' ','') in B.name_words: #om rubriken på ena är i andras channel rack
            set_same.add(A.filename)
            poäng +=1
        if len(A.name_words) > len(B.name_words): #om den ena har fler filer än den andra
            poäng += 1
        return set_same, poäng
    
    for word in A.name_words:
        if word in B.name_words:
            set_same.add(word)
    #hitta om A är äldre än B:
    if A.c_time < B.c_time: 
        set_same, poäng = checker(A, B)
    elif B.c_time < A.c_time:
        set_same, poäng = checker(B, A)
    
    p = poäng//3 * 100
    return set_same, p

def identify_similar(folder_path): #helst vill jag att den ska cluster likadana projekt ihop
    for project, i in folder_path:
        pass

def find_ends(A, B):
    ändelser = [f"v{i}" for i in range(1,10)] + ['beat', 'final', 'beat', 'edit', 'copy']
    pass

def main(folder_path):
    mapp = parsing(folder_path)
    project1 = mapp[0]
    project2 = mapp[1]
    orden, poäng = find_similar(project1, project2)
    """for i in enumerate(mapp):
        orden, poäng = find_similar(mapp[i], mapp[i+1])""" #dehär går inte, den måste kunna "cluster" project som är lika på nåt sätt
    print('\n-----TEST FOLDER-----\n')
    print(f"-----{project1.filename}----- \n {len(project1.hash)} hashar \n, ord: {project1.name_words},\n plugins: {project1.plugins}\n")
    print(f"-----{project2.filename}----- \n {len(project2.hash)} hashar \n, ord: {project2.name_words} ,\n plugins: {project2.plugins}\n")
    print('\n-----------')
    print(f"de hashen som är likadana är {project1.hash.intersection(project2.hash)}")
    print(f"de orden som är likadana {orden}, och sannolikheten att {project1.filename} är förälder till {project2.filename} är {poäng}‰")

if __name__ == "__main__":
    main('/Users/amir/Downloads/CodeAmir/DD1333/test')

"""
hur kan man lättast avgöra om ett projekt är förälder till ett annat?
1. om ena av projekten innehåller en fil som har samma namn som 
"""