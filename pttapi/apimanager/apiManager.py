'''
Created on 25 jul. 2018

@author: isanlui
'''
 
from pttapi.apimanager.authptt import authptt
from pttapi.utils.log import mylogging
from pttapi.utils.files import ensure_dir
import json


import requests
import os


class apiManager():
    def __init__(self,pttconfig,apiname):        
        self.mauth=None 
        self.pttconfig=pttconfig
        self.configschema=self.__getSchema()
        self.apiname=apiname
        self.stage="apimanager"
        self.setCredentialsFromConfig(self.__getCredentials())  
        
    
    def __getCredentials(self):
        if isinstance(self.pttconfig,dict):
            return {"username":self.pttconfig.get("auth",{}).get("user") ,
                "password":self.pttconfig.get("auth",{}).get("password"),                
                "permisionlist":self.pttconfig.get("auth",{}).get("permisionlist",[]) }
        else:
            return self.pttconfig.getCredentials()
        
    
    def __getSchema(self):
        if isinstance(self.pttconfig,dict):
            return {
            "url":"%s/:stage/:type"%self.pttconfig.get("api",{}).get("url","https://dev-api.plug2teams.com"),
            "x-api-key":"%s"%self.pttconfig.get("api",{}).get("x-api-key","-") , 
            "auth":{"url":"%s/auth"%self.pttconfig.get("auth",{}).get("url","https://dev-api.plug2teams.com") ,
                "x-api-key":"%s"%self.pttconfig.get("auth",{}).get("x-api-key","-"),
                "apiname":self.pttconfig.get("api",{}).get("name","-") }  
            }
        
        else:            
            return self.pttconfig.getSchemaForApi()
    
    
    def __getURLBase(self,mytype="data"):              
        return self.configschema.get("url").replace(":stage",self.stage).replace(":type",mytype)
       
    
    def __getURLAPI(self,mytype="data"):
        return "%s/%s"%(self.__getURLBase(mytype),self.apiname )  
    
    
    def getEntityList(self):                
        r=requests.get(self.__getURLAPI(),headers=self.mauth.getAuthHeaders(xapikey=self.configschema["x-api-key"]))
        if r.status_code ==200:
            return r.json()
        else:
            mylogging(message="[ERROR] getEntityList, status:%s description:%s"%(r.status_code,r.text), level="ERROR", pr=False)
            return None
        
    
    def getAPIList(self):        
        r=requests.get(self.__getURLBase(),headers=self.mauth.getAuthHeaders(xapikey=self.configschema["x-api-key"]))
        if r.status_code ==200:
            return r.json()
        else:
            mylogging(message="[ERROR] getAPIList, status:%s description:%s"%(r.status_code,r.text), level="ERROR", pr=False)
            return None
        return None
    
    
    
    def setCredentials(self,user,password,permisionlist=[]):        
        credentials={"username": user,"password":password,"permisionlist":permisionlist}
        self.mauth=authptt(self.configschema["auth"]).setCredentials(credentials=credentials)                
        return self
    
    def setCredentialsFromConfig(self,pttcont):                
        if pttcont is not None:
            return self.setCredentials(
                user=pttcont["username"],
                password=pttcont["password"],
                permisionlist=pttcont.get("permisionlist",[]))
        
        return self
    
    def Entity(self,name):        
        return self.getEntity(name)
    
    def getEntity(self,name):
        if self.mauth is None:
            self.mauth.getAuth()
        
        if self.mauth is not None:
            return apiptt(config=self.configschema,
                      apiname=self.apiname,
                      entityname=name,
                      stage=self.stage,
                      myauth=self.mauth)
        else:
            mylogging("(getEntity) Not authrntificated user",level="ERROR",pr=True)
            return None
    
            
        
        



class apiptt(object):
    '''
    classdocs
    '''
    
    def __init__(self, config,apiname,entityname,stage="api",myauth=None):
        '''      Constructor       '''
        
        self.entityname=entityname
        self.configschema=config.copy()
        self.apiname=apiname
        self.configschema["stage"]=stage        
        self.configschema["stage"]=stage        
        self.setTest(activate=False)  
        self.mauth=myauth       
    
    def __makeException(self,description,requestreturn):
        pass
                
    def __getURLBase(self,mytype="data"):              
        return self.configschema.get("url").replace(":stage",self.configschema.get("stage")).replace(":type",mytype)
       
    def __getURLAPI(self,mytype="data"):
        return "%s/%s"%(self.__getURLBase(mytype),self.apiname )
    
    def __getURLItem(self,mytype="data"):        
        return "%s/%s"%(self.__getURLAPI(mytype),self.entityname)
    
    
    
    def setEntuty(self,entityname):
        self.entityname=entityname
    
    
    
    def setTest(self,activate):
        self.test=activate
    
    
    
        #:lang/invoxapi/client/:id"
    def getApiKey(self,apikey):
        return  self.configschema["x-api-key"]
    
        
    def getItemList(self):
        r=requests.get(self.__getURLItem(),headers=self.mauth.getAuthHeaders(xapikey=self.configschema["x-api-key"]),params=None)
        if r.status_code ==200:            
            return r.json()
        else:
            mylogging(message="[ERROR] getting item list, status:%s description:%s"%(r.status_code,r.text), level="ERROR", pr=False)
            return None
        
        
    def getItem(self,itemid):
        murl="%s/%s"%(self.__getURLItem(),itemid)        
        #print("myurl:%s"%murl)        
        r=requests.get(murl,headers=self.mauth.getAuthHeaders(xapikey=self.configschema["x-api-key"]))
        if r.status_code ==200:
            return r.json()
            mylogging(message="[ERROR] getting item, status:%s description:%s"%(r.status_code,r.text), level="ERROR", pr=False)
        else:
            mylogging(message="[ERROR] getting item, status:%s description:%s"%(r.status_code,r.text), level="ERROR", pr=False)
            return None
        
    
    def getItemByIdName(self,idname,itemid):
        murl="%s/%s?idname=%s"%(self.__getURLItem(),itemid,idname)        
        #print murl
        r=requests.get(murl,headers=self.mauth.getAuthHeaders(xapikey=self.configschema["x-api-key"]))
        if r.status_code ==200:
            return r.json()
        else:
            mylogging(message="[ERROR] getting item by name, status:%s description:%s"%(r.status_code,r.text), level="ERROR", pr=False)
            raise Exception('spam   56565 eggs')
            return None
    
    def __setItem(self,myobject,itemid=None,params=None):
        payload = json.dumps(myobject)        
        if itemid is None:
            myurl=self.__getURLItem(mytype="data")
        else:
            myurl="%s/%s"%(self.__getURLItem(mytype="data"),itemid)        
        
        r=requests.post(myurl, data=payload,headers=self.mauth.getAuthHeaders(xapikey=self.configschema["x-api-key"]),params=params)        
        
        if r.status_code ==200:
            return r.json()
        else:
            mylogging(message="[ERROR] setting item, status:%s description:%s"%(r.status_code,r.text), level="ERROR", pr=False)
            return None
    
    def __updateItem(self,myobject,itemid=None,params=None):
        if "id" in myobject:
            del  myobject["id"]

        payload =json.dumps(myobject)    
            
        if itemid is not None:
            myurl="%s/%s"%(self.__getURLItem(mytype="data"),itemid)
            r=requests.patch(myurl, data=payload,headers=self.mauth.getAuthHeaders(xapikey=self.configschema["x-api-key"]),params=params)
            if r.status_code ==200:
                return r.json()
            else:
                mylogging(message="[ERROR] updating item status:%s description:%s"%(r.status_code,r.text), level="ERROR", pr=False)
                
        
        return None
    
    def __deleteItem(self,myobject=None,itemid=None,params=None):
        payload = json.dumps(myobject)
        myurl="%s/%s"%(self.__getURLItem(mytype="data"),itemid)
        r=requests.delete(myurl,data=payload,headers=self.mauth.getAuthHeaders(xapikey=self.configschema["x-api-key"]),params=params)
        if r.status_code ==200:
            return r.json()
        else:
            mylogging(message="[ERROR] deleting item status:%s description:%s"%(r.status_code,r.text), level="ERROR", pr=False)
            return None
     
    
    def createItem(self,myobject,owner=None):
        if owner is not None:
            params={"account_id":owner}
        else:
            params=None
        
        return self.__setItem(myobject=myobject,itemid=None,params=params)
    
    def createFileItem(self,filename,description=None,mytype="general",owner=None):
        """mytype general/music/voive"""        
        if os.path.isfile(filename): 
            myobject={"filename":os.path.basename(filename),
                      "description":description if description is not None else os.path.basename(filename).replace(".mp3","").strip(),
                      "type":mytype
                      }
            ret=self.__setItem(myobject=myobject,itemid=None,params=None)
            if isinstance(ret,dict):
                if ret.get("result",False):
                    if ret.get("response",{}).get("count",0)>0:
                        data=ret.get("response",{}).get("items",[])[0].get("data",{})
                        
                        """if "x-amz-security-token" in data['fields']:
                            del data['fields']["x-amz-security-token"]"""
                        
                        with open(filename, 'rb') as f:
                            files = {'file': (filename, f)}
                            http_response = requests.post(data.get('url'), data=data.get('fields'), files=files)
                            
                        print("http_response:%s status_code:%s"%(http_response.text,http_response.status_code))
                        if http_response.status_code >210:
                            return {"result":False,
                                    "error":http_response.text,
                                    "status_code":http_response.status_code,
                                    }
                        else:
                            return {"result":True,"id":ret.get("response",{}).get("items",[])[0]["id"]}
            else:
                return {"result":False,"error":"error setting item %s"%filename}
        else:
            return {"result":False,"error":"invalid file %s"%filename}
        
    def downLoadFileItem(self,itemid,filename=None):         
        ret=self.getItem(itemid)
        if ret.get("result",False):
            if ret.get("response",{}).get("count",0)>0:
                download=ret.get("response",{}).get("items",[])[0].get("download",{})
                url=download.get("url") if download.get("result",False) else None
                if url is not None:
                    if filename is None:
                        filename=ret.get("response",{}).get("items",[])[0].get("data",{}).get("filename",None)
                    
                    r = requests.get(url)
                    if ensure_dir(filename):
                        
                        f = open(filename, 'wb')
                        for chunk in r.iter_content(chunk_size=512 * 1024): 
                            if chunk: # filter out keep-alive new chunks
                                f.write(chunk)
                        f.close()
                        return {"filename":filename}
        return None
        
          
           
    
    def updateItem(self,myobject,itemid,owner=None):
        if owner is not None:
            params={"account_id":owner}
        else:
            params=None
        
        return  self.__updateItem(myobject,itemid=itemid,params=params)
    
    def createRelation(self,itemid,relationlist,owner=None):
        if "-" in self.entityname:
            if owner is not None:
                params={"account_id":owner}
            else:
                params=None
            items=[]
            for item in relationlist:
                items.append({"id":item})
            if len(items)>0:
                myobject={"items":items}   
                return self.__setItem(myobject,itemid=itemid,params=params) 
        return None
    
    def addRelation(self,itemid,relationlist,owner=None):
        if "-" in self.entityname:
            if owner is not None:
                params={"account_id":owner}
            else:
                params=None
            items=[]
            for item in relationlist:
                items.append({"id":item})
            if len(items)>0:
                myobject={"items":items}   
                return self.__updateItem(myobject,itemid=itemid,params=params) 
        return None
    
    def deleteRelation(self,itemid,relationlist,owner=None):
        if "-" in self.entityname:
            if owner is not None:
                params={"account_id":owner}
            else:
                params=None
            items=[]
            for item in relationlist:
                items.append({"id":item})
            if len(items)>0:
                myobject={"items":items}   
                return self.__deleteItem(myobject,itemid=itemid,params=params) 
        return None
        
    def Action(self,action,actiondata,owner=None):
        if owner is not None:
                params={"account_id":owner}
        else:
            params=None
        
        myurl=self.__getURLItem(mytype="action")
        myobject={"action":action,"actiondata":actiondata}        
        payload = json.dumps(myobject)
               
        r=requests.post(myurl, data=payload,headers=self.mauth.getAuthHeaders(xapikey=self.configschema["x-api-key"]),params=params)        
        if r.status_code ==200:
            return r.json()
        else:
            mylogging(message="[ERROR] Executing action, status:%s description:%s"%(r.status_code,r.text), level="ERROR", pr=False)
            return None  
        return None    
    
    
    def deleteItem(self,itemid,owner=None):
        if owner is not None:
            params={"account_id":owner}
        else:
            params=None       
       
        return self.__deleteItem(myobject=None,itemid=itemid,params=params)
    
    
        
                
    







        