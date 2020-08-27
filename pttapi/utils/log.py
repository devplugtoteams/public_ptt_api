#!/usr/bin/env python
# encoding: utf-8
'''
Created on 8/4/2015

@author: isanlui
'''
import os
from optparse import OptionParser
import logging
from datetime import datetime
import traceback
import sys

try:
    import syslog
    SYSLOGLOADED=True
except:
    SYSLOGLOADED=False
    pass
try:
    LAMBDAFUNCTION= (os.environ.get('LAMBDAFUNCTION',"false")=='true')
except:
    LAMBDAFUNCTION=False

USESYSLOG=SYSLOGLOADED and not LAMBDAFUNCTION



def safe_str(obj):
    """ return the byte string representation of obj """
    PY2=False    
    basestring = str
    
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        mylogging("safe_str error", pr=True)
        return obj
        

def start_logger(myfile):
    parser = OptionParser(add_help_option=False)
    parser.add_option("--help",   help="--show help and exit", action="store_true", dest="myhelp", default=False)
    parser.add_option("-h",   help="--show help and exit", action="store_true", dest="myhelp", default=False)
    parser.add_option("--log",   help="--log --> set level log - values: debug,info,warning,error,critical", action="store", dest="loglevel", default="WARNING")
    parser.add_option("--logfile",   help="--logfile -->show log in file if present  if not then show log in console", action="store_true", dest="logfile", default=False)
    parser.add_option("--syslog",   help="--logfile -->show log in file if present  if not then show log in console", action="store_true", dest="logfile", default=False)
    try:
        (options, args) = parser.parse_args()
        loglevel=options.loglevel.upper()
        console=not options.logfile
        myhelp=options.myhelp
        
    except :
        logging.error ('[1] Failed to parse params -> setting default values   '  )
        myhelp=False
        loglevel="WARNING"
        console=True
        parser.print_help()
        
    if(myhelp):
        parser.print_help()
        return False
          
    numeric_level = getattr(logging, loglevel, None)
    
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
        numeric_level = getattr(logging, "INFO", None)
        logging.error('Invalid log level: %s , changing to INFO' % loglevel )
    
    
    if(console):
        logging.basicConfig(format='%(levelname)s:(%(asctime)s):  %(message)s',level=numeric_level)
        #logging.basicConfig(format='%(message)s',level=numeric_level)
    else:
        logging.basicConfig(format='%(message)s',level=numeric_level,filename=myfile.replace('.py',''))
        
    return True

def getloglevel(level):
    """LOG_ALERT, LOG_EMERG,   LOG_CRIT,  LOG_ERR,  LOG_WARNING,  LOG_NOTICE,  LOG_INFO, LOG_DEBUG"""
    return {"LOG_ALERT":syslog.LOG_ALERT,
     "LOG_EMERG":syslog.LOG_EMERG,
     "LOG_CRIT":syslog.LOG_CRIT,
     "LOG_ERR":syslog.LOG_ERR,
     "LOG_WARNING":syslog.LOG_WARNING,
     "LOG_NOTICE":syslog.LOG_NOTICE,
     "LOG_INFO":syslog.LOG_INFO,
     "LOG_DEBUG":syslog.LOG_DEBUG,
     
     "ALERT":syslog.LOG_ALERT,
     "EMERG":syslog.LOG_EMERG,
     "CRITICAL":syslog.LOG_CRIT,
     "CRIT":syslog.LOG_CRIT,
     "ERR":syslog.LOG_ERR,
     "ERROR":syslog.LOG_ERR,
     "WARNING":syslog.LOG_WARNING,
     "NOTICE":syslog.LOG_NOTICE,
     "INFO":syslog.LOG_INFO,
     "DEBUG":syslog.LOG_DEBUG         
        }.get(level,syslog.LOG_WARNING)

def mylogging(message,level="LOG_WARNING",pr=False):
    myloggin(message,level,pr)
    
def myloggin(message,level="LOG_WARNING",pr=False):
    """LOG_ALERT, LOG_EMERG,  LOG_ALERT,  LOG_CRIT,  LOG_ERR,  LOG_WARNING,  LOG_NOTICE,  LOG_INFO, LOG_DEBUG"""
    
    if pr is True:
        try:
            print( "(%s): %s"%(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),message) )
        except:
            print ("************Loggin error**********************")            
    try:
        if USESYSLOG:
            syslog.syslog(getloglevel(level),"IBMSG %s" % message)
        elif pr is False:
            print( "(%s): %s"%(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),message) )
    except:
        try :        
            syslog.syslog(syslog.LOG_ERR,"[ERROR] log -controlado- IBMSG %s" % safe_str(message))
        except:
            print( "[ERROR] log -controlado- (%s): %s"%(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),message) )
            pass
        #logging.error(safe_str(message))


def mylogginException(message=None):
    try:            
        mylogging(message=traceback.format_exc(),pr=True)
        if message is not None:
            mylogging(message="Traceback:%s"%message,pr=True)
    except Exception as e:
        mylogging(message="traceback.format_exc() error:%s"%e,pr=True)
       

def mylogginginfo(message,level=syslog.LOG_INFO):
    """LOG_ALERT, LOG_EMERG,  LOG_ALERT,  LOG_CRIT,  LOG_ERR,  LOG_WARNING,  LOG_NOTICE,  LOG_INFO, LOG_DEBUG"""
    try:
        syslog.syslog(level,"IBMSG %s" % message)
    except:
        logging.info(message)
    
    
