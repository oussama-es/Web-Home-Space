from pymongo import MongoClient
from model import Departement,Prof
client=MongoClient('mongodb://localhost:27017')
class DepartementDao:
    def __init__(self,db,collection) -> None:
        self.db=client[db]
        self.collection=self.db[collection]
    def findByName(self,name:str)->Departement:
        document=self.collection.find_one({'name':name})
        if document!=None :
            return Departement(**document)
        return None
    def findById(self,id:int)->Departement:
        document=self.collection.find_one({'_id':id})
        if document!=None :
            return Departement(**document)
        return None
    def listProfsByDepartement(self,dep_id:int)->list[Prof]:
        document=self.collection.find_one({'_id':dep_id},{'_id':0,'profs':1})
        profs:list[Prof]=[]
        for prof in document['profs']:
            profs.append(Prof(**prof))
        return profs
    def listAllDepartement(self)->list[Departement]:
        if self.collection.count_documents!=0 :
            departements=self.collection.find()
            list_deps:list[Departement]=[]
            for dep in departements :
                list_deps.append(Departement(**dep))
            return list_deps
        else :
            return []
    def createDepartement(self,dept:Departement)->bool:
        result=self.collection.find_one(vars(dept))
        if result :
            return False
        self.collection.insert_one(vars(dept))
        return True
    def findProfByEmail(self,email:str)->Prof:
        profs_dict=self.collection.find_one({'profs.email':email},{'_id':0,'profs':1})
        if profs_dict==None :
            return None
        else :
            for prof in profs_dict['profs']:
                if prof['email']==email:
                    return Prof(**prof)
        
    def addProfToDepartement(self,dep_id:int,prof:Prof):
            result=self.collection.update_one({'_id':dep_id},{'$push':{'profs':vars(prof)}})
            return result.modified_count==1
    def deleteDepartement(self,id:int)->bool:
        result=self.collection.delete_one({'_id':id})
        return result.deleted_count == 1 
        
    def deleteProfFromDepartement(self,dep_id:int,prof:Prof):
        result=self.collection.update_one({'_id':dep_id},{'$pull':{'profs':vars(prof)}})
        return result.modified_count == 1
    
    def updateProfFromDepartement(self,dep_id:int,prof:Prof)->bool:
        result=self.collection.update_one({'_id':dep_id,'profs.email':prof.email},{'$set':{'profs.$':vars(prof)}})
        return result.modified_count==1
