from dataclasses import dataclass,field

@dataclass
class Prof:
    name:str
    email:str

@dataclass
class Departement:
    _id:int
    name:str
    #afin que la liste soit initialisee par [] par defaut
    profs:list[Prof]=field(default_factory=lambda : [])
        
    