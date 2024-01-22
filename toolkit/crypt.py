import os
import re
import base64
import random
import string
from   pathlib       import Path
from   Crypto.Cipher import AES
from   Crypto        import Random
try:
  from ._version import version as __version__
except ImportError:
  __version__ = 'unknown'


class Cipher:
  """
  Usage:
  from awi.cyrpt import Cipher
  aes = Cipher()
  print(aes.passwd("PASSWORD('hCzbGkjpdLxgCP8YwsTNJcnIcMBFlKbKwgXWNkuZPM6kbeYyoqV6NjoMv9Ijtemp')"))

  aes = Cipher(key[:16], 32)
  enc = aes.encrypt('ppppppppppppppppppppppppppppppppppppppppppppppppppppppp')
  msg = aes.decrypt(enc)
  print("'{}'".format(msg))
  """
  
  def __init__(self, blk_sz=32):
    """ 
    Construct a new Cipher object. 
    :param key:     An optional 16 character string of salt
    :param blk_sz:  An option size for the buffer (default: 32)
    :return:        Reference to Cipher
    """
    self.key    = self._get_key()
    self.blk_sz = blk_sz

  def encrypt(self, raw):
    """
    Encrypts string 'raw' using AES 
    
    :param raw:    A string to be encrypted
    :return:       void
    """
    if raw is None or len(raw) == 0:
      raise NameError("No value given to encrypt")
    raw = raw + '\0' * (self.blk_sz - len(raw) % self.blk_sz)
    raw = raw.encode('utf-8')
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(self.key.encode('utf-8'), AES.MODE_CBC, iv)
    return base64.b64encode( iv + cipher.encrypt( raw ) ).decode('utf-8')

  def decrypt(self, enc):
    """
    Decrypts a raw unformatted encrypted string

    :param enc:  An encrypted string to decrypt
    :return:     string
    """
    if enc is None or len(enc) == 0:
      raise NameError("No value given to decrypt")
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(self.key.encode('utf-8'), AES.MODE_CBC, iv)
    return re.sub(b'\x00*$', b'', cipher.decrypt( enc[16:])).decode('utf-8')

  def passwd(self, str):
    """
    Decrypt a formatted string.

    In order to differentiate password strings from encrypted password strings,
    Cipher recognizes a config file format like this: PASSWORD('lksjflsjfljsflfsjlfsjlkj') 
    Use this method to parse the encrypted string and return a decrypted string.
    plain = aes.password("PASSWORD('lksjflsjfljsflfsjlfsjlkj')")

    :param str:  A string formated as follows PASSWORD('encrypted-string')
    :return:     Decrypted password string

    """
    if str.startswith("PASSWORD(") :
      ons = str.find('PASSWORD(') + 9
      end = str.find(')', ons)
      res = str[ons:end].replace("'", "")
      res = res.replace("\"", "")
      pwd = self.decrypt(res)
      return pwd
    else:
      return str

  def _get_key(self):
    home = str(Path.home())   
    name = "{}/.razr".format(home)

    if os.path.exists(name):
      with open(name) as f:
        lines = f.read().splitlines() 
      for line in lines:
        if len(line) == 16: return line  
    else:
      key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
      try:
        fp = open(name, 'w')
      except IOError:
        print("Unable to open and write to the output file: %s", name)
        fp.close()
        exit(1)
      finally:
        fp.write("{}\n".format(key))
        fp.close()
      return key
 
