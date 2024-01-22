import io
import sys
import os
import random
import string
import time
from   datetime  import date, datetime as dt, timedelta

try:
  from ._version import version as __version__
except ImportError:
  __version__ = 'unknown'

class StringBuffer(object):
  """
  A mutable sequence of characters. A StringBuffer is like a str, but can be modified. 
  At any point in time it contains some particular sequence of characters, but the length 
  and content of the sequence can be changed through certain method calls. 

  """
  def __init__(self) -> None:
    """ 
    Constructor: StringBuffer()

    Parameters:
    None

    Returns:
    StringBuffer
    """
    self._stringio = io.StringIO()

  def append(self, *objects, sep=' ', end='') -> None:
    """
    Append a series of objects to the StringBuffer

    Parameters:
    objects (varied):    A series of objects, primitives, etc. to append to the StringBuffer
    sep(char):           [Optional] A character to separate the objects Default: ' '
    end(char):           [Optional] A character to end the objects. Default '' Generally a newline ('\n')

    Returns:
    StringBuffer
    """
    print(*objects, sep=sep, end=end, file=self._stringio)

  def substring(self, begin: int, end: int) -> str:
    """
    Returns a new String that contains a subsequence of characters currently contained within 'begin' and 'end'.

    Parameters:
    begin(int):          The starting position of the substring
    end  (int):          The ending position of the substring

    Returns:
    substring(str):      A substring between (and including) the charaters from 'begin' to 'end'
    """
    if begin > end:
      raise ValueError("\nUsage: sb.substring(begin, end)\nError: begin cannot be greater than end")
    string = self._stringio.getvalue()
    first  = begin if begin > 0 and begin < len(string) else 0
    last   = end   if end   < len(string) else len(string)
    return string[first:last]

  def toString(self) -> str:
    """
    Returns a string representing the data in this sequence.

    Parameters:
    None

    Returns:
    String               A string representation of this series of characters.
    """
    return self.__str__()
 
  def __str__(self) -> str:
    return self._stringio.getvalue()


class Quarter:

  @staticmethod
  def number(day:date) -> int:
    """
    For day(date) return an int 1-4 which represents the yearly quarter

    Parameters:
    day(date):      A date for which we need the quarter

    Returns:
    qtr(int):       An int representing the quarter number
    """
    try:
      return (day.month-1)//3 + 1
    except (ValueError, TypeError, AttributeError):
      print("Date format: mm-dd-yyyy")

  @staticmethod
  def start(qtr:int) -> date:
    """
    Returns the starting date of qtr(int)

    Parameter
    qtr(int):       The number of the yearly quarter

    Returns:
    day(date):      The date of the quarter start (01-01-yyyy, 04-01-yyyy, 07-01-yyyy, 10-01-yyyy)
    """
    day  = date.today()
    year = day.year
    soq  = {
      1:date(year,1,1),
      2:date(year,4,1),
      3:date(year,7,1),
      4:date(year,10,1)
    }
    return soq[qtr]

  @staticmethod
  def week(day:date) -> int:
    """
    Returns the week number of the quarter for input day

    Parameters:
    day (date):     The day for which we want to find the week number of the quarter

    Returns:
    int:            The week number of the quarter
    """
    year = day.year
    soq  = {
      1:date(year,1,1),
      2:date(year,4,1),
      3:date(year,7,1),
      4:date(year,10,1)
    }
    for i, sow in enumerate(soq[Quarter.number(day)]+timedelta(weeks=x) for x in range(5*3)):
      if sow>=day:
        return i+1

  @staticmethod
  def nextSunday(day:date) -> date:
    """
    For date day returns the next date of the next Sunday. If day is a Sunday, it will return day

    Parameters:
    day(date):      The date for which we want the next Sunday

    Returns:
    sunday(date):   The next Sunday or parameter day if day is a Sunday
    """
    sundays = {
      "Monday"    : day+timedelta(6),
      "Tuesday"   : day+timedelta(5),
      "Wednesday" : day+timedelta(4),
      "Thursday"  : day+timedelta(3),
      "Friday"    : day+timedelta(2),
      "Saturday"  : day+timedelta(1),
      "Sunday"    : day+timedelta(0)
    }
    return sundays[day.strftime('%A')] 

  def sundays(day:date) -> list:
    """
    Returns a list of 13 Sundays for the quarter beginning on parameter day

    Parameter:
    day(date):      The start of the quarter

    Returns
    list[dates]:    A list of dates (Sundays)
    """
    s = day
    r = []
    for i in range(13):
      day = Quarter.nextSunday(s)
      r.append(day)
      s = day + timedelta(days=2)
    return r

class Timer:
  """ 
  Tracks the time between Timer.start and Timer.stop and returns an elapsed
  time in seconds
  """
  def __init__(self):
    self._start = None
    self._stop  = None

  def tid(self):
    """
    Returns a unique 17 character Transaction ID
    
    :param: none 
    :return int: unique transaction ID 
    """
    return int(round(time.time() * 1000000))

  def sleep(self, num):
    """
    Pause execution for num seconds

    :param int: Number of seconds for which to sleep
    :return:    void
    """
    time.sleep(num)

  def start(self, datestr=None):
    """
    Set the timer to start and capture that moment or set the timer to start
    with optional datestr in the following format: '2020-11-16 21:12:11'
 
    :param:  datestr - OPTIONAL in the following format '%Y-%m-%d %H:%M:%S'
    :return: void
    """
    if datestr == None:
      self._start = time.time() 
    else:
      day = dt.strptime(datestr, '%Y-%m-%d %H:%M:%S')
      self._start = day.timestamp()
    
  def stop(self):
    """
    Stop the timer and capture the moment
    
    :param: void
    :return None:    
    """
    self._stop = time.time()

  def elapsed(self):
    """
    Return the elapsed time between start() and stop()

    :param: None
    :return float: the elapsed time in milliseconds
    """
    return (self._stop - self._start)

class Random(object):
  """
  Reads a column formatted config file which may contain hash (#) comments
  The parser strips leading and trailing white space along with new line 
  characters. 
  """
  @staticmethod
  def string(length=10):
    """
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

class Extension(object):
  """
  A class with static methods for doing file extension operatiosn
  """
  
  @staticmethod
  def unique(path):
    """
    Extenstion.unique(path) 
    
    Returns a unique file name based on the path. If 'path' exists, it adds
    an integer to the end of the name. If path.N exits, it increments the 
    integer by one. If path/file contains path/file.1, path/file.2 then 
    uniquify(path) will return path/file.3

    :param path:    A fully qualifiled path to file, i.e., '/home/jdfulmer/src/haha.c'
    :return string: A unique filename 
    """
    if os.path.isfile(path):
      num = 0
      new = path
      while True:
        num += 1
        if os.path.isfile(new):
          res = res = path.rsplit('.',1)
          ext = (res[len(res)-1])
          new = "{}.{}".format(path, num)
          continue
        else:
          return new
    else:
      return path

