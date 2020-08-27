'''
Created on 6 abr. 2020

@author: isidoro
'''
#!/usr/bin/env python
# encoding: utf-8
'''
isi_utils -- shortdesc

isi_utils is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2015 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

"""import sys
import os
import types
import re"""
import json
from decimal import Decimal
import uuid
from datetime import datetime,date
from pttapi.utils.log import myloggin,mylogginException
import random
import string
#from imemcached import fromMemcached,toMencached
#import memcache
 

import io

PY2=False
basestring = str

   

def isNumber(mynumber):
    return isinstance(mynumber,(int,float,complex))
    
    
def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        return obj

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))   

def getBytesFromString(mystr):    
    if isinstance(mystr,str):        
        try:
            return mystr.encode('utf-8')
        except:
            mylogginException()
            pass
    return mystr

def getStringFromBytes(mybytes):
    if isinstance(mybytes, bytes):
        try:
            return mybytes.decode('utf-8')
        except:
            mylogginException()
            pass
    return mybytes

def defaultencode(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, Decimal):
        return ("%s"%obj)
    if isinstance(obj, (datetime, date)):
        return obj.strftime('%s') #  isoformat()
    if isinstance(obj,uuid.UUID):
        return obj.hex
        
    if isinstance(obj, bytes):
        try:            
            return obj.decode('utf-8') #  isoformat()
        except:
            pass
    raise TypeError ("Type %s not serializable" % type(obj))

    


    
    

def getJsonnice(myjson):
    if myjson is not None:
        if isinstance(myjson,dict) is not True:
            if isinstance(myjson,list) is not True:
                myjson=json_to_object(myjson)            
        return (json.dumps(myjson, indent=4, sort_keys=True,default=defaultencode))
    return "{}"

def printJson(myjson):
    print(getJsonnice(myjson))


    

def mydecode1(mystring):
    try:
        return mystring.decode('ascii').encode('utf-8','ignore')
    except UnicodeDecodeError:
        try:
            return mystring.decode('latin-1','ignore').encode('utf-8','ignore')
        except UnicodeDecodeError:
            return mystring
 
   

def json_to_object(myjs):
    """ transforms a json string  into a list or a dict
    @param myjs= json strting
    @return object (list , dict) if error return None
    """
    if myjs is not None:        
        try:
            return json.loads(myjs)
        except:
            try:
                myloggin("json_to_object ERROR ->%s"%myjs,pr=True)
                mylogginException(message=None)
                return None
            except:
                myloggin("json_to_object ERROR",pr=True)
                mylogginException(message=None)
                return None   
    return None

def object_to_json(myobj,nice=False):
    """ transforms a object (dict,list) into a JSON string
    @param myobj= object to transform (list , dict) 
    @return Json String , None if error
    """
    
    if myobj is not None:        
        if isinstance(myobj,basestring):
            return None # parser error
        elif isinstance(myobj,str):
            
            return None # parser error
        else:
            myobj=vars(myobj)
        if not nice:           
            return json.dumps(myobj,default=defaultencode)
        else:
            return json.dumps(myobj, indent=4,default=defaultencode ,sort_keys=True)
    else:
        
        return None
    

def myint(number,default=0):
    """ return a int from a  object
    @param number object to convert into a integer    
    @param default default value if error (0)
    @return integer
    """
    try: 
        return int(number)
    except:
        return default

def myintRange(number,default=0,minvalue=None,maxvalue=None):
    ret_=myint(number=number,default=default)
    if minvalue is not None:
        if ret_<minvalue:
            ret_=minvalue
    if maxvalue is not None:
        if ret_>maxvalue:
            ret_=maxvalue
    return ret_



