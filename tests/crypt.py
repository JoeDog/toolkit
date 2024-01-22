import sys
import os
import unittest
import pprint
import logging
sys.path.insert(0, os.path.dirname(
  __file__)+"/.."
)
from toolkit.crypt import Cipher

class TestOne(unittest.TestCase):
  PASSWORD  = None
  ENCRYPTED = None

  def test_1_encrypt(self):
    """
    Encrypt a password then decrypt it and check for a match
    """
    aes = Cipher()
    TestOne.ENCRYPTED = aes.encrypt(TestOne.PASSWORD) 
    if TestOne.PASSWORD in aes.decrypt(TestOne.ENCRYPTED):
      res = "True"
    else:
      res = "False"
    print("%s [%s]" % (("Encrypting %s and checking result" % TestOne.PASSWORD).ljust(63, '.'), res))


  def test_2_password(self):
    """
    Format the encrypted password in PASSWORD('lksjlsj;lfkjsflwioueoitjjlsjls;fj') format 
    then check aes.passwd parser to ensure the unencrypted passwords match
    """
    aes = Cipher()
    tmp = "PASSWORD('{0}')".format(TestOne.ENCRYPTED)
    pwd = aes.passwd(tmp) 
    if TestOne.PASSWORD in pwd:
      res = "True"
    else:
      res = "False"
    print("%s [%s]" % ("Parsing PASSWORD('') format and checking result".ljust(63, '.'), res))


if __name__ == '__main__':
  TestOne.PASSWORD = 'hahapapa'
  unittest.main(verbosity = 0)
