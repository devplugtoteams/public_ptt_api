'''
Created on 18 ago. 2020

@author: isidoro
'''
import sys
sys.path.append('../')
from pttapi.apimanager.apiManager import apiManager
from pttapi.utils.utils import printJson
import time

pttconfig=None

pttconfig=pttconfig={
    "api": {
        "name": "wmt",
        "url": "https://dev-api.plug2teams.com",
        "x-api-key": "jaIB1UBX2K5OHDBRVsdX04erc46nP2La7MaVKQMT"
    },
    "auth": {
        "user": "berlinguyinca@gmail.com",
        "password": "Ad%drtR45TY#MUtFr43SrG^KFcqXMhGO73fphN#8*@Gtr4R",  #"your password here",
        "url": "https://dev-api.plug2teams.com",
        "x-api-key": "J5ioIZgsAp9hH1cElyQf73YRNTttOJML6vYi7nys"
    }
}

apimngr=apiManager(pttconfig=pttconfig,apiname="wmt")

# objectypelist 
print("----------------------------------getEntityList---------------------------------")
resp=apimngr.getEntityList()
printJson(resp)


# getItemList 
print("----------------------------------getItemList entity indicator---------------------------------")

resp=apimngr.Entity("indicator").getItemList()
printJson(resp)

# getItem 
print("----------------------------------getItem---------------------------------")
resp=apimngr.Entity("indicator").getItem(itemid="SMA7")
printJson(resp)

print("----------------------------------getItemByIDName---------------------------------")
resp=apimngr.Entity("indicator").getItemByIdName(idname="parameters.field",itemid="close")
printJson(resp)

start=time.time()
end=start+3600*2
i=0
while end>time.time():    
    print("----------------------------------CreateItem---------------------------------")
    """ If id is not indicated then system generate a random ID (uuid) """
    myobject={
               "description": "Simple Moving Average period ...",
               #"id": "SMA_%s"%i, 
                "name": "SMA",
                "parameters": {
                     "field": "close",
                     "timeperiod": 9
                    }
            }
    
    
    resp=apimngr.Entity("indicator").createItem(myobject,owner=None)
    printJson(resp)    
    time.sleep(3)
    
    if resp.get("result",False): 
        if resp.get("response",{}).get("count",0)>0:      
            id=resp.get("response",{}).get("items",[])[0].get("id")
            print("DeleteItem --> %s"%id)
            if id is not None:
                resp=apimngr.Entity("indicator").deleteItem(itemid=id,owner=None) 
                printJson(resp)
