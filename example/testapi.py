'''
Created on 18 ago. 2020

@author: isidoro
'''
#import sys
#sys.path.append('../')
from pttapi.apimanager.apiManager import apiManager
from pttapi.utils.utils import printJson

pttconfig=None

pttconfig={
    "api": {
        "name": "wmt",
        "url": "url to api",
        "x-api-key": "api key value"
    },
    "auth": {
        "user": "user",
        "password": "Ad%drtR45TY#MUtFr43SrG^KFcqXMhGO73fphN#8*@Gtr4R",  #"your password here",
        "url": "url to api",
        "x-api-key": "auth api key"
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

exit()
print("----------------------------------CreateItem---------------------------------")
""" If id is not indicated then system generate a random ID (uuid) """
myobject={
           "description": "Simple Moving Average period ...",
           "id": "SMA9", 
            "name": "SMA",
            "parameters": {
                 "field": "close",
                 "timeperiod": 9
                }
        }


resp=apimngr.Entity("indicator").createItem(myobject,owner=None)
printJson(resp)

print("----------------------------------UpdateItem---------------------------------")
myobject={
        "description":"Simple Moving Average period 9"
        }
resp=apimngr.Entity("indicator").updateItem(myobject,itemid="SMA9",owner=None)
printJson(resp)

print("----------------------------------DeleteItem---------------------------------")

resp=apimngr.Entity("indicator").deleteItem(itemid="SMA9",owner=None) 
printJson(resp)


