'''
Created on 6 abr. 2020

@author: isidoro
'''
import os
import time

from pttapi.utils.log import mylogging, mylogginException
from pttapi.utils.utils import object_to_json, json_to_object


def getBasePath(lastpath="ptt"):
    lastpath="/%s"%lastpath
    mypath=os.path.dirname(os.getcwd())
    n=0
    while not mypath.endswith(lastpath):
        mypath=os.path.dirname(mypath)
        n=n+1
        if n>4:
            return os.path.dirname(os.getcwd())
    return mypath

def load_file(filename):
    """ load a text file.
    @param filename = name of file
    @return string whith text file content 
    """
    ret_=";"
    try:
        myfile = open(filename, 'r')
        ret_= myfile.read()
        myfile.close()
    except:
        ret_=";"
    return ret_;
    

def get_my_path():
    """ Return the path of python script
    @return path string   
    """
    return os.path.dirname(os.path.realpath(__file__))

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    print("-------->%s"%directory)
    if directory is not None:
        if len(directory)>0:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                    return True
                except:
                    mylogging("ensure_dir error %s"%directory, pr=True)
                    return False
                    pass
            else:
                return True
        else:
            return True
    return False

def download_streaming_file(url,filename):
    try:
        import requests
    except:
        from botocore.vendored import requests
    local_filename = filename
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    if ensure_dir(local_filename):
        with open(local_filename, 'wb+') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
            r.close()
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename


def createDictFile(filename,jsondata,duration):
    if isinstance(jsondata, (dict,list)):
        data={
            "data":jsondata,
            "created_at":int(time.time()),
            "expire":int(time.time())+duration            
            }
        try:                      
            ensure_dir(filename)
            mylogging(message="creatinf File : %s"%filename, level="INFO", pr=False)
            with open(filename, "w") as text_file:
                text_file.write(object_to_json(data))
            return True            
        except :
            mylogginException()                    
            return False
    return False

def getFileAsDict(filename):        
    if filename is not None:        
        mylogging(message="getting item from file cached %s"%filename,  pr=False) 
        try:
            with open(filename, 'r') as myfile:
                data = myfile.read()
            configdata=json_to_object(data) 
            if isinstance(configdata, dict):
                if configdata.get("expire")>time.time()-1:       
                    return  configdata.get("data",None)
        except FileNotFoundError:
            return None
        except:
            mylogginException()
            mylogging(message="getConfigFileAsDict [ERROR] %s"%filename,level="ERROR",  pr=False)
            
        return None