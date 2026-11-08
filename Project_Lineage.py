import pyflp
import os
import hashlib
from music21 import key, pitch
import librosa as lb
class Project():
    def __init__(self, filepath, filename, channels, patterns, mixer, arrangements, tempo):
        
        self.filepath: str = filepath
        self.filename: str = filename
        self.m_time: float = os.path.getmtime(filepath)
        self.c_time: float = os.path.getctime(filepath)
        
        self.hash: set[str] = set()
        self.name_words: set[str] = set()
        self.plugins: set[str] = set()
        
        #Trädrelationer
        self.parent = None
        self.children = []
        
        self.channels: set[str] = channels
        self.patterns = patterns
        self.mixer = mixer
        self.arrangements = arrangements
        self.tempo = tempo

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
                
                project = Project(filepath, name, flp.channels, flp.patterns, flp.mixer, flp.arrangements, tempo) #avvakta med len(flp.channels) för nu
                
                project.hash = add_hashes
                
                project.name_words = name_words
                project.name_words.add(name)
                
                project.plugins = plugins
                
                projects.append(project)
            except Exception as e:
                print(f"Couldn't read the file {filename}: {e} ")
    return projects

def hashes(flp):
    
    def signature(channel):
            full_sample_path = str(channel.sample_path)
            try: #om den sökvägen finns på datorn
                with open(full_sample_path, "rb") as f: #läser in samplet som binär fil
                    md5 = hashlib.md5()
                    sample = f.read()
                    md5.update(sample)
                    return md5.hexdigest()
                
            except Exception: 
                if full_sample_path:
                    return None 
            return None
    
    add_hashes = set()
    for channel in flp.channels:
        if hasattr(channel, "sample_path") and channel.sample_path:
            md5hash = signature(channel)
            if md5hash:
                add_hashes.add(md5hash)
    
    return add_hashes

def find_name_words(flp):
    name_words = set()
    plugins = set()
    for channel in flp.channels:
        if channel.name:
            name_words.add(channel.name.replace(" ","").lower())
        if hasattr(channel, 'plugin') and channel.plugin:
            plugins.add(channel.plugin.name)
    return name_words, plugins

def find_key(flp):
    pass

#1. är den ena äldre än den andra
#2. är namnet på den ena i orden på den andra
#3. har de gemensamma ord
#4. har den ena fler kanaler än den andra
#5. finns det gemensamma hashar
#6. har de samma key
#7. har de samma tempo

def checker(A, B):
    tot_points = 0
    set_same = set()
    n_criteria = 7
    
    if A.c_time < B.c_time:
        tot_points = float(get_points(A, B, set_same)/n_criteria)
    
    else:
        tot_points = float(get_points(B, A, set_same)/n_criteria)
    
    return tot_points, set_same

def get_points(A,B,s):
    A_name = A.filename.replace(' ','')
    B_name = B.filename.replace(' ','')
    A_nchannels = len(A.channels)
    B_nchannels = len(B.channels)
    
    s.add("time created")
    points = 1
    
    if B_name in A.name_words:
        points +=1
        s.add("name in project")
    
    if len(A.name_words.intersection(B.name_words)) > 0:
        points +=1
        s.add("similar words")
    
    if A_nchannels <= B_nchannels:
        points +=1
        s.add("more channels")
    
    if len(A.hash.intersection(B.hash)) > 0:
        points +=1
        s.add("same hashes")
    
    #key kommer sen
    
    if A.tempo == B.tempo:
        points +=1
    
    return points

def main(folder_path):
    s = set()
    mapp = parsing(folder_path)
    project1 = mapp[0]
    project2 = mapp[1]
    print(f"{project1.channels}, |{project1.patterns}, |{project1.mixer}, |{project1.arrangements}")
    print('\n-----TEST FOLDER-----\n')
    print(f"-----{project1.filename}----- \n {len(project1.hash)} hashar \n, ord: {project1.name_words},\n plugins: {project1.plugins}\n")
    print(f"-----{project2.filename}----- \n {len(project2.hash)} hashar \n, ord: {project2.name_words} ,\n plugins: {project2.plugins}\n")
    print('\n-----------')
    print(f"de hashen som är likadana är {project1.hash.intersection(project2.hash)}")
    print(checker(project1, project2))

if __name__ == "__main__":
    main('/Users/amir/Downloads/CodeAmir/DD1333/test')

"""
hur kan man lättast avgöra om ett projekt är förälder till ett annat?
1. om ena av projekten innehåller en fil som har samma namn som 
"""