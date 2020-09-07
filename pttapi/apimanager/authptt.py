'''
Created on 25 jul. 2018

@author: isanlui
'''

import json
import time

from pttapi.utils.log import myloggin, mylogginException
from pttapi.utils.utils import object_to_json
import requests


class authptt(object):

    actiontypes=["auth","auth.s1","auth.s2","refresh","signup"]

    def __init__(self, config=None):
        """{"url":"https://api.plug2talk.com/auth" , "x-api-key" "apiname":"pttapi" } """
        self.config=config        
        self.authdict=None
        self.credentials=None
        self.code=None
        
        
    def __setCode(self,code):
        #self.__setAuth({"code":code})
        if isinstance(code,dict):
            if "code" in code:
                self.code=code["code"]
                return True
        return False
    
    def getCode(self):
        return self.code
    
    def setCredentials(self,credentials):
        #{"username": username,"password":password,"permisionlist":permissionlist }
        self.credentials=credentials
        self.authdict=None
        """self.credentials["payload"]= object_to_json({"username":self.credentials["username"]
                                                    ,"password":self.credentials["password"],
                                                    "permisionlist":self.credentials["permisionlist"] })"""
        
        
        return self
    
    def __getApiket(self):
        return self.config.get("x-api-key")
        
    def getURL(self,mtype):
        if mtype in self.actiontypes:
            return "%s/%s/%s"%(self.config["url"],mtype,self.config.get("apiname","pttapi"))
        return None    
                       
            
    def __getAuthHeaders(self):
        return {
            "Content-Type":"application/json",        
            "x-api-key":self.__getApiket()
            }
    
    def __validAuthDict(self,authdict=None):
        
        if authdict is None:
            authdict=self.authdict
        
        if isinstance(authdict, dict):
            if(authdict.get("result",False)):
                for item in ["ExpiresIn","RefreshToken","IdToken","Expire","ExtraToken"]:
                    if item not in authdict:
                        return False
                return True
        return False               
    
    
    def __setAuthdict(self,authfromrequest):
        self.code=None
        if self.__validAuthDict(authfromrequest):  
            myloggin(message="auth credentials renewed : ok", level="INFO", pr=True)                              
            self.authdict=authfromrequest
            return True
        return False
        
    def auth(self):
        
        if self.credentials is not None:           
            r=requests.put(self.getURL("auth"),
                           data=json.dumps(self.credentials),  #object_to_json(self.credentials),
                           headers=self.__getAuthHeaders())
            if self.__setAuthdict(r.json()):
                return r.json()            
        return None 
    
    def auths1(self):
        self.authdict=None
        self.code=None
        if self.credentials is not None:
            r=requests.put(self.getURL("auth.s1"),data=json.dumps(self.credentials),headers=self.__getAuthHeaders())
            if self.__setCode(r.json()):            
                return r.json()
        return None 
    
    def auths2(self):
        code=self.getCode()
       
        if code is not None:
            data='{"code":"%s"}'%code            
            r=requests.put(self.getURL("auth.s2"),data=data,headers=self.__getAuthHeaders())            
            if self.__setAuthdict(r.json()):
                return r.json()
        return None
    
          
    def refresh(self):
        myloggin(message="refresh auth", level="INFO", pr=True)
        if self.credentials is not None:
            if self.__validAuthDict():            
                myloggin(message="refreshing auth credentials :  url:%s "%self.getURL("refresh"), level="INFO", pr=True)
                payload={"RefreshToken":self.authdict.get("RefreshToken","-")}
                myloggin(message="payload:%s "%payload, level="INFO", pr=True)
                
                r=requests.put(self.getURL("refresh"),data=json.dumps(payload),headers=self.__getAuthHeaders())
                newauth=None
                if r is not None:
                    newauth=r.json()
                    if isinstance(newauth, dict):
                        if newauth.get("result",False):
                            myloggin(message="Renew ok ", level="INFO", pr=True)
                            if self.__setAuthdict(r.json()):
                                return r.json()
                
                myloggin(message="[ERROR] Can't renew Oath tokens %s"%("request errr" if newauth is None else newauth), level="INFO", pr=True)
                            
                #myloggin(message="authdict:%s "%r.json(), level="INFO", pr=True)
                
            else:
                myloggin(message="Refresh authdict not valid %s"%self.authdict, level="ERROR", pr=True)
        return None
    
    def getAuth(self):        
        if self.authdict is None:            
            self.auth()            
        if self.authdict is not None:            
            if self.authdict.get("Expire",0)<=int(time.time())+15:                
                myauth=self.refresh()                
                if myauth is None:
                    self.auth()
                    
                
         
        return self.authdict
            
        pass
    
    """def getValue(self,name):
        return self.getAuth().get(name)"""
    
    
    def getAuthHeaders(self,xapikey,test=False):        
        if test:
            ret_ ={"Authorization":"Bearer %s"%self.getAuth().get("IdToken","-"),
            "Content-Type":"application/json",
            "isitest":"hola",
            "x-api-key":xapikey}
        else:         
            ret_= {"Authorization":"Bearer %s"%self.getAuth().get("IdToken","-"),
            "Content-Type":"application/json",
            "x-api-key":xapikey}    
         
        return ret_
        
        

        


    
    