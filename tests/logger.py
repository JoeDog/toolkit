import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(
  __file__)+"/.."
)

from toolkit.logger import Simple
from toolkit.logger import Syslog
from toolkit.logger import Splunk
from toolkit.util   import Timer

"""
Will this 
"""

class TestLog(unittest.TestCase):

  def test_1_simple(self):
    log = "/tmp/logger.log"
    ret = Simple.log(log, "log_1_simple test from toolkit source directory")
    res = "True" if ret == True  else "False"
    print("%s [%s]" % (("Write to log '%s' and assert true" % log).ljust(63, '.'), res))

  def test_2_syslog(self):
    test = Syslog.log('localhost', Syslog.Severity.debug.value, 'This is a test')
    print("%s [%s]" % (("Write to syslog server and assert true").ljust(63, '.'), True))

if __name__ == '__main__':
  unittest.main(verbosity = 0)
