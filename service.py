from typing import Any
from model import Prof,Departement
from dal import DepartementDao


class DepartementService:
    def __init__(self) -> None:
        self.dao=DepartementDao('school','depart')
    def createDepartement(self,dep:Departement) :
        #check inputs, if ok
        #check if departement exist
        if self.dao.findByName(dep.name)!=None:
            self.dao.createDepartement(dep)
        else :
            return dep.name + ' already exist'
    def addProfToDepartement(self,dep_id:int,prof:Prof)->Any:
        #check inputs, if ok
       
        #check if prof exist 
        if self.dao.findProfByEmail(prof.email)==None :
        #if all its ok then add prof
            return self.dao.addProfToDepartement(dep_id,prof)
        else :
            return prof.email + ' already exist'
    def ListDepartementByName(self,name:str)->list:
        dept=self.dao.findByName(name)
        profs=vars(dept)['profs']
        return profs

    def listDepartements(self)->list:
        return self.dao.listAllDepartement()
