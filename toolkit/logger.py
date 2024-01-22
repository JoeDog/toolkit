import sys    
import os
import fcntl
import inspect
import logging
import logging.handlers
import datetime
import platform
import requests
from enum import Enum

try:
  from ._version import version as __version__
except ImportError:
  __version__ = 'unknown'

class Simple(object):
  """
  Writes date and message to a log file
  """
  @staticmethod
  def log(filename, msg, **kwargs):
    """ 
    Writes a message to a local file.
 
    Parameters:
      filename (str) - Name of the file including it's path, i.e., /var/log/awesome.log
      msg (str)      - The message that we want to log, i.e. 'Internal error' 

    Keywords:
      Not supported for this method
    
    Return:
      result (bool)  - True on success, False on failure
    """
    stack = inspect.stack()
    calling_class  = "Simple" # stack[1][0].f_locals["self"].__class__.__name__
    calling_method = "log"    # stack[1][0].f_code.co_name
    # Aug  2 03:36:17 lccns344 puppet-master[28110]:
    exe = os.path.basename(sys.argv[0]) # the calling program
    pid = os.getpid()
    srv = platform.node().split('.', 1)[0]
    res = True
    try:
      f = open(filename, 'a+')
      fcntl.lockf(f, fcntl.LOCK_EX)
      data = ("%s %s %s %s[%d]  %s\n" %
               (
                 datetime.datetime.now().strftime("%b %d %H:%M:%S"),
                 ('{}.{}'.format(calling_class, calling_method)),
                 srv,
                 exe,
                 pid,
                 msg
               )
             )
      f.write(data)
    except Exception as error:
      print("    UNABLE to open: %s\n    %s" % (filename, error))
      res = False
    else:
      fcntl.lockf(f, fcntl.LOCK_UN)
      f.close()
      if kwargs:
        if kwargs['verbose'] == True:
          print(data)
    return res

class Syslog():
  """
  Send log message via syslog
  """
  class Severity(Enum):
    debug    = 10
    info     = 20
    warning  = 30
    error    = 40
    critical = 50

  @staticmethod
  def log(server, severity, message, **kwargs): 
    """
    Send data to syslog server
  
    Parameters:
      server (str)   - The syslog server to which the data is posted
      severity (int) - Int representation of log level encapulated in an Enum, i.e., Syslog.Severity.debug.value
      message (str)  - The message portion of the syslog posting, i.e., 'Big trouble in Little China'

    Keywords:
      udp_port (int) - Overrides the default port (514)
      
    Return:
      void 
    """
    stack = inspect.stack()
    calling_class  = "Syslog" # stack[1][0].f_locals["self"].__class__.__name__
    calling_method = "log"    # stack[1][0].f_code.co_name

    if kwargs:
      port = kwargs['udp_port']
    else:
      port = 514
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler(address=(server, port))
    formatter = logging.Formatter('{}.{}: %(message)s'.format(calling_class, calling_method))
    handler.setFormatter(formatter)
    log.addHandler(handler)

    log.log(severity, message)

class Splunk():
  """
  Send log message to Splunk via HTTP event collector
  """  

  @staticmethod
  def hec(instance, tid, tgroup, taction, **kwargs): #kwargs - tevent, ttask
    """
    Posts JSON data to splunk

    Parameters:
      instance (str)  - The splunk server's hostname. Applies to {}.joedog.org
      tid (int)       - A unique identifier. You probably want awi.util.Timer.tid() for this field 
      tgroup (str)    - The associated ServiceNow group, i.e., hosting, network, etc.
      taction (str)   - The action performed (build, hostmaster, etc.)

    Keyworks:
      index (str)     - Use this keyword to override the default index (fs-automation)
      token (str)     - Use this keyword to override the default token for the default index
                        Other keywords are task related, snow_taks='SCTASK999999', ip_add='192.168.0.1' etc.

    Return:
      result (bool)   - True on success, False on failure
    """
    requests.packages.urllib3.disable_warnings()
    url        = 'https://{}.joedog.org:8088/services/collector/event'.format(instance)
    token      = (kwargs.get('token') if kwargs.get('token') is not None else "99473e2c-bfed-4845-9cd7-f4b2358012f6")
    index      = (kwargs.get('index') if kwargs.get('index') is not None else "fs-automation")
    authHeader = {'Authorization': 'Splunk {}'.format(token)}
    event      = {
      'TID'     : tid,
      'TGROUP'  : tgroup,
      'TACTION' : taction
    }

    # This is a catch-all for additional kwargs
    if kwargs:
      for k, v in kwargs.items():
        if k == "index" or k == "token":
          continue
        else:
          event[k] = v

    jsn = {"index":index, "event":event} 
    req = requests.post(url, headers=authHeader, json=jsn, verify=False)
   
    if req.status_code == 200: 
      return True
    else: 
      print(req.status_code, req.text)
      return False      
