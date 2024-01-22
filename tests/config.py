import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(
  __file__)+"/.."
)

from toolkit.config import Column, Columns, Slurp, INI, Block

class TestTwo(unittest.TestCase):

  def test_1_col(self):
    col = Column.read(TestTwo.FILEONE)
    num = len(col)
    tmp = os.path.basename(TestTwo.FILEONE)
    res = "True" if num == 15 else "False"
    print("%s [%s]" % (("Read %s and assert fifteen lines" % tmp).ljust(63, '.'), res))

  def test_2_cols(self):
    cols = Columns.read(TestTwo.FILETWO, sep='|')
    deep = len(cols)
    wide = len(cols[0])
    tmp  = os.path.basename(TestTwo.FILETWO)
    res  = "True" if deep == 6 and wide == 2 else "False"
    print("%s [%s]" % (("Read %s and assert six lines and two cols" % tmp).ljust(63, '.'), res))

  def test_2_ini(self):
    tmp    = os.path.basename(TestTwo.FILETHR)
    ini    = INI.read(TestTwo.FILETHR, sep='=')
    tst    =  [False for i in range(5)]
    tst[0] = True   if len(ini['default']['username']) == 16 else False
    tst[1] = True   if ini['default']['password'].startswith("PASSWORD(") else False
    tst[2] = True   if len(ini['vcenters']) == 5 else False
    tst[3] = True   if len(ini['excludes']) == 4 else False
    tst[4] = True   if len(ini['pirates'])  == 9 else False 
    print("%s [%s]" % (("Read %s and assert five traits" % tmp).ljust(63, '.'), False not in tst))

  def test_3_slurp(self):
    cfg    = os.path.basename(TestTwo.FILEFOU)
    tmp    = Slurp.read(TestTwo.FILEFOU)
    res    = "True" if 'file_content' in tmp else "False"
    print("%s [%s]" % (("Read %s and assert one trait" % cfg).ljust(63, '.'), res))

  def test_4_block(self):
    tmp    = os.path.basename(TestTwo.FILEFIV)
    blk    = Block.read(TestTwo.FILEFIV, sep='=')
    tst    = 0
    for host, data  in sorted(blk.items()):
      if host == 'default' or host.startswith("lab"):
        tst = tst+1
    res    = "True" if tst == 4 else "False"
    print("%s [%s]" % (("Read %s and assert four matches" % tmp).ljust(63, '.'), res))
  
  def test_5_variable(self):
    tst    = "/tmp/spring-2020"
    cfg    = os.path.basename(TestTwo.FILESIX)
    ini    = INI.read(TestTwo.FILESIX)
    var    = ini.get('commands').get('cmd')
    res    = "True" if tst in var else "False"
    print("%s [%s]" % (("Read %s and assert variable evaluation" % cfg).ljust(63, '.'), res))
 
if __name__ == '__main__':
  TestTwo.FILEONE = os.path.dirname(os.path.realpath(__file__))+"/../etc/1.conf"
  TestTwo.FILETWO = os.path.dirname(os.path.realpath(__file__))+"/../etc/2.conf"
  TestTwo.FILETHR = os.path.dirname(os.path.realpath(__file__))+"/../etc/3.conf"
  TestTwo.FILEFOU = os.path.dirname(os.path.realpath(__file__))+"/../etc/4.txt"
  TestTwo.FILEFIV = os.path.dirname(os.path.realpath(__file__))+"/../etc/5.conf"
  TestTwo.FILESIX = os.path.dirname(os.path.realpath(__file__))+"/../etc/6.conf"
  unittest.main(verbosity = 0)

