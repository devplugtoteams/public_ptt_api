'''
Created on 18 sept. 2018

@author: isanlui
'''

from pttapi.utils.utils import myint
from pttapi.utils.log import myloggin 

class apiresult():
    RESPONSE="response"
    REQUEST="request"
    ITEMS="items"
    COUNT="count"
    RESULT="result"
    LASTEVALUATEDKEY="lastevaluatedkey"
    ERROR="error"
    INFO="info"
    
    
    
    def __init__(self,copydict=None):
        """
        @param myresult: dict with a standar result format
        {"result":True/False,"error":error message,"request":{},"response":{"items":[],count:integer ,'lastevaluatedkey'} 
        """
        
        self.tesult={self.RESULT:False,self.RESPONSE:{}}
        if copydict is not None:
            if not self.setFromDict(copydict):
                self.tesult={self.RESULT:False,self.RESPONSE:{}}
            
    
    def checkValifDict(self,resultdict):
        for item in [self.RESULT,self.RESPONSE]:
            if item not in resultdict:
                myloggin("(checkValifDict) non valid result %s"%resultdict)
                return False
        return True
    
    def setFromDict(self,resultdict):
        if self.checkValifDict(resultdict):
            self.tesult=resultdict 
        else:
            myloggin("(setFromDict) result not set")          
        return self
        
    
    def __checkResult(self):
        pass
    
    def validresult(self):
        return self.tesult[self.RESULT]
    
    def response(self):
        return self.tesult.get(self.RESPONSE,{})
    
    def request(self):
        return self.tesult.get(self.REQUEST,{})
    
    def count(self):
        if self.validresult():
            return myint(self.response().get(self.COUNT,0))
        return 0
    def lastevaluatedkey(self):
        return self.response().get(self.LASTEVALUATEDKEY)
    
    def appendResult(self,newresult):
        if newresult is not None:
            if newresult.count()>0:
                if self.count()==0:
                    self=newresult
                else:                    
                    for item in newresult.getItems():                    
                        self.addItem(item)
                                        
                pass
                
    def __getSimple(self): 
        
        """ Solo por compatibilidad quitar cunado marcio implemente el standard"""
        resp2={}
        for item in self.tesult:                
            if item==self.RESPONSE:
                for item1 in self.response():
                    resp2[item1]=self.response()[item1]
            else:
                resp2[item]=self.tesult[item]
        return resp2
            
        """ Solo por compatibilidad quitar cunado marcio implemente el standard"""           
    
    def get(self,simple=False):
        """
        to do: create a get with filters for example to eliminate some values 
        "ResponseMetadata": ---> HTTPHeaders
        """
        if simple:
            return self.__getSimple()
        else:
            return self.tesult
    def getReturn(self):
        if "ResponseMetadata" in self.request():
            if "HTTPHeaders" in self.request()["ResponseMetadata"]:
                del self.request()["ResponseMetadata"]["HTTPHeaders"]
        return self.get()
                
            
        
    def getItems(self):
        if self.count()>0:
            return self.response().get(self.ITEMS)
        return []
    
    def getItem(self,index=0):
        items=self.getItems()
        if len(items)>index:
            return items[index]
        return None
    
    
    def addItem(self,item):
        if self.tesult[self.RESPONSE].get(self.ITEMS) is None:
            self.tesult[self.RESPONSE][self.ITEMS]=[]
        
        self.tesult[self.RESPONSE][self.ITEMS].append(item)
        self.tesult[self.RESPONSE][self.COUNT]=len(self.tesult[self.RESPONSE][self.ITEMS])
        
            
        pass
        
    
        
    def setItems(self,items,count=None,lastevaluatedkey=None): 
        if self.RESPONSE not in  self.tesult:
            self.tesult[self.RESPONSE]={}                    
        
        if isinstance(items,list) is False:
            if isinstance(items,dict):
                if len(items)==0:
                    items=[]
                else:
                    items=[items]
            elif items is None:
                items=[]
            else:
                items=[items]
                    
                
        if count is None:
            count =len(items)
        if count==0:
            items=[{}]
        
        
        self.tesult[self.RESPONSE][self.ITEMS]=items           
        self.tesult[self.RESPONSE][self.COUNT]=count
        if lastevaluatedkey is not None:
            self.tesult[self.RESPONSE][self.LASTEVALUATEDKEY]=lastevaluatedkey
        return self
    def setResponse(self,response):
        if isinstance(response, dict):
            self.tesult[self.RESPONSE].update(response)
        return self
        
    
    def setResult(self,result,errormesg=""):                
        
        self.tesult[self.RESULT]=result
        if errormesg is not None:
            if len(str(errormesg))>1:
                self.tesult[self.ERROR]=errormesg
        return self
         
    
    def setRequest(self,request):
        self.tesult[self.REQUEST]=request
        return self
    def getSchema(self):
        return {self.RESULT:"boolean true or false",
         self.ERROR:"(optional) description of error if result is true",
         
         self.RESPONSE:{
                self.ITEMS:"[array of items] (mandatory for GET requests)",
                self.COUNT:"number of returned itemen , if 0 , no items returned (mandatory for GET requests)",
                self.LASTEVALUATEDKEY:"(optional) {dict whith last key evalute , valid for pagination}",
                self.INFO:"{} dictionary with info about request in (PUT,POST,PATCH,DELETE requests) (optional)"
                
                
        
             
             },
         self.REQUEST:"{} optional information about request"
         }
        
        
        
        
        
    
            
        
    