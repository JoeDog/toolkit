import os
import sys
import unittest
from   datetime import datetime as dt, date
sys.path.insert(0, os.path.dirname(
  __file__)+"/.."
)
from toolkit.util import Random, Extension, Timer, Quarter, StringBuffer

class TestRPC(unittest.TestCase):

  def test_random(self):
    siz = 12
    tmp = Random.string(siz)
    num = len(tmp)
    res = True if num==siz else False
    print("{0} [{1}]".format(("Generate %d char random string: %s " % (siz, tmp)).ljust(63, '.'), res))
  
  def test_extension(self):
    pwd = "/etc/passwd"
    new = Extension.unique(pwd)
    res = True if new not in pwd else False
    print("{0} [{1}]".format(("Generate a unique name for %s: %s " % (pwd, new)).ljust(63, '.'), res))
   
  def test_timer_dynamic(self):
    timer = Timer()
    timer.start()
    timer.sleep(1)
    timer.stop()
    dur = timer.elapsed()
    res = True if dur > 1.0 else False
    print("{0} [{1}]".format(("Testing dynamic timer delay %2.8f " % (dur)).ljust(63, '.'), res))
    
  def test_timer_static(self):
    timer = Timer()
    timer.start('2023-05-12 14:13:00')
    timer.stop()
    dur = timer.elapsed()
    res = True if dur > 1.0 else False
    print("{0} [{1}]".format(("Testing static timer delay %2.8f " % (dur)).ljust(63, '.'), res))
    
  def test_quarter(self):
    qtr = Quarter.number(date.today())
    day = Quarter.start(2)
    sun = Quarter.sundays(day)
    res = True if len(sun) == 13 else False
    print("{0} [{1}]".format(("Testing quarter for %d sundays " % (len(sun))).ljust(63, '.'), res))
  
  def test_string_buffer(self):
    ts = "New York Jets"
    sb = StringBuffer() 
    sb.append("New", "York", "Jets")
    res = True if ts in str(sb) else False
    print("{0} [{1}]".format(("Testing for '%s' in StringBuffer " % (ts)).ljust(63, '.'), res))
   
if __name__ == '__main__':
  unittest.main(verbosity = 0)

