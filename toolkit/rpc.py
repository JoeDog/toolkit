import os
import platform
from   os.path    import expanduser
from   subprocess import Popen, PIPE
from   awi.util   import Random
from   awi.crypt  import Cipher

try:
  from ._version import version as __version__
except ImportError:
  __version__ = 'unknown'


class SSH(object):
  """
  Allows you to execute remote procedure calls
  """
 
  #-oPasswordAuthentication=no 
  def __init__(self, hostname, username, password='', sshkey='', timeout=10, enablepw='no'):
    """
    Construct a new rpc.SSH object
    rpc = SSH('jeff', 'tops3cr3t', 'labas009.joedog.org')
    rpc.run('ls /')

    NOTE: If enablepw is set to 'yes' and your script encounters a server
    on which the account is not present, it will hang indefinitely. 
    
    :param hostname:  An optional 16 character string of salt
    :param username:  An option size for the buffer (default: 32)
    :param password:  An optional passphrase for the key or the server
    :param sshkey:    Path to ssh private key; uses $HOME/.ssh/id_rsa by default 
    :param timeout:   An int value for the connection timeout (default 10)
    :param enablepw:  An option which allows server password logins (default no)
    :return:          Reference to an rpc.SSH object
    """
    self.hostname = hostname
    self.username = username
    if password.startswith("PASSWORD("):
      aes = Cipher()
      self.password = aes.passwd(password)
    else:
      self.password = password
    self.sshcmd   = (
      "ssh -o StrictHostKeyChecking=no -o ConnectTimeout=%d -o PasswordAuthentication=%s -t" % (timeout, enablepw)
    )
    self.sshkey   = sshkey
    self.homedir  = os.path.expanduser('~'+self.username)
    self.prompt   = ""
    self.login    = ""
    self.command  = ""
    self.tmpfile  = ("/tmp/%s" % Random.string(18))

    if not self.username:
      print("ERROR: A username is required to complete this function")
      exit(1)

    if not self.hostname:
      # XXX: Do we want this? We could use this to run local commands
      print("ERROR: A hostname is required to complete this function")
      exit(1)

    self.login   = ("%s@%s" % (self.username, self.hostname))

    if self.password:
      tmp = self.password
      cmd = "where" if platform.system() == "Windows" else "which"
      prc = Popen([cmd, 'sshpass'], stdout=PIPE, stderr=PIPE)
      prc.communicate()
      if prc.returncode != 0:
        print("ERROR: Failed awi.rpc.SSH dependency.")
        print("       The password option requires 'sshpass' which is not installed on")
        print("       this system. Run: 'yum install sshpass' to satisfy the requirement.")
        exit(1)
      self.password = "sshpass -f \"%s\"" % self.tmpfile
      try:
        with open(self.tmpfile, "w") as f:
          f.write(tmp)
      except Exception as error: 
        print("ERROR: Unable to cache password")
      
    if not self.sshkey:
      self.sshkey = "%s/.ssh/id_rsa" % self.homedir
      f = None
      try:
        f = open(self.sshkey)
      except IOError:
        print("ERROR: Unable to access private key: %s" % self.sshkey)
        self.sshkey = ""
      finally:
        if f is not None:
          f.close()
    tmp = self.sshkey
    if tmp and tmp.strip():
      self.sshkey  = ("-i %s" % tmp)
    else:
      self.sshkey = ""

    if self.password and self.sshkey:
      self.prompt = "-P \"id_rsa':\""
    else:
      self.prompt = ""

    # sshpass -p 'password' -P "id_rsa':" ssh -o StrictHostKeyChecking=no user@host 'command'
    # self.password self.sshcmd self.login
    self.command = ("%s %s %s %s %s" % (self.password, self.prompt, self.sshcmd, self.sshkey, self.login)) 
    #print(self.command)

  def run(self, cmd):
    """
    run a command and capture the output. 

    NOTE: Generally cmd is a string representing a command that will be run on a remote server.
    If cmd is /bin/ls /etc/passwd then execution is 'ssh name@server /bin/ls /etc/passwd' But if
    cmd contains a pipe, then it's split between local and remote execution. Consider this cmd:
    "echo 'password' | sudo passwd --stdin jdfulmer" that will be executed like this:
    echo 'password' | ssh name@server sudo passwd --stdin jdfulmer

    :param cmd:  An option which allows server password logins (default no)
    :return:     A string output from the cmd
    """
    pre = ""
    if "|" in cmd:
      arr = cmd.split('|', 1)
      pre = "{}|".format(arr[0])
      cmd = arr[1]
    tmp    = ("%s%s %s" % (pre, self.command, cmd))
    stream = os.popen(tmp)
    output = stream.read()
    stream.close()
    return output

  def __del__(self):
    if os.path.exists(self.tmpfile):
      os.remove(self.tmpfile)
   
    

