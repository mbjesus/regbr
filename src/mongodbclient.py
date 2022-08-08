from pymongo import MongoClient

class MongoDbClient:
    
    def __init__(self):
        self.host = 'mongodb://:@:/'
        self.client = -1
        self.databaseDict = {}
        self.collectionDict = {"test":123}
        
    def connnect(self):
        if self.client == -1:
            #Creating a pymongo client
            self.client = MongoClient(self.host)

    def getConnection(self):
        return self.client
    
    def getDatabase(self,databaseName):
        
        if self.client == -1:
            self.connnect()
            
        if databaseName not in self.databaseDict.keys():
            self.databaseDict[databaseName] = self.client[databaseName]
        
        return self.databaseDict[databaseName]
    
    def getCollection(self,databaseName,collectionName):
        
        if collectionName not in self.collectionDict.keys():
            
            database = self.getDatabase(databaseName)
            #Creating a collection
            self.collectionDict[collectionName] = database[collectionName]
        
        return self.collectionDict[collectionName]
      
    def close(self):
        if self.client != -1:
            self.client.close()