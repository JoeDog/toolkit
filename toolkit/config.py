import csv
import re
import os.path
try:
  from ._version import version as __version__
except ImportError:
  __version__ = 'unknown'

class MalformedVariableError(Exception):
  def __init__(self, error, line):
    Exception.__init__(self,
      '\n    ERROR: Malformed variable in config file' +
      '\n    Should be formatted like $(section.name)'+
      '\n    {}\n    LINE: {}'.format(error, line)
    )


class Column(object):
  """
  Reads a column formatted config file which may contain hash (#) comments
  The parser strips leading and trailing white space along with new line 
  characters. 
  """
  @staticmethod
  def read(name):
    """
    Read a file which contains a column of data. The file may contain
    hash # comments. Leading and trailing white space will be stripped
    from the column. 

    Usage example:
    from awi.config import Column

    col = Column.read('/path/to/file')
    if len(col) < 1:
      print("ERROR: Unable to read /path/to/file")
    else:
      for word in col:
        print(word)

    :param name:  String path to the config file
    :return:      list of lines from the file
     
    """
    with open(name, 'r') as f:
      content = f.readlines()

      lines=[]
      for line in content:
        newline  = line.replace('\n','')
        location = newline.find('#')
        if location >= 0: # if the line has no comment, location is -1
          newline = newline[0:location].strip()
    
        # append if line is not empty
        if newline is not '':
          lines.append(newline)
    return lines

  @staticmethod
  def exists(name):
    return os.path.exists(name)

class Columns(object):
  """
  Columns - Reads a character separated config file and returns a multidimensional array
  of the colummns in the file. The parser recognizes UNIX style hash (#) comments and it
  trims leading and trailing white space
  """
  @staticmethod
  def read(name,sep=","):
    """
    Read a formatted config file which contains columns separated by a character. 
    The default separator is comman but you can choose any character for separation.
     
   
    Usage example:

    from awi.config import Columns

    cols = Columns.read('/path/to/file', sep='|')
    for i in range(len(cols)):
      for j in range(len(cols[i])):
        ret = '\\n' if j == 1 else '\\t'
        print(cols[i][j], end=ret)

    :param name:  String - full path to the config file
    :param sep:   Character (optional) - The column separator in the file (default comma)
    :return:      Multidimensional array 
    """
    lines=[]
    with open(name, 'r') as csvfile:
      content = csv.reader(csvfile, delimiter = sep)
      for line in content:
        if len(line) < 1:
          continue
        if line[0].find('#') >= 0:
          continue
        row=[]
        for col in line:
          location = col.find('#')
          if location >= 0: # if the line has no comment, location is -1
            col = col[0:location].strip()
          if col is not '':
            row.append(col.strip())
        if ''.join(row).strip():
          lines.append(row) 
    return lines

  @staticmethod
  def exists(name):
    return os.path.exists(name)

class Slurp(object):
  """
  Slurp - Reads the whole file (including comments) into a string
          s = Slurp.read('filename')
  """
  @staticmethod 
  def read(name):
    with open(name, 'r') as f:
      content = f.read()
    return str(content) 

  @staticmethod
  def exists(name):
    return os.path.exists(name)

class INI(object):
  """
  INI - Reads and parses an INI style configuration file. The parser honors UNIX style
  hash (#) comments and it trims leading and trailing white space. 
  """
  @staticmethod
  def _dequote(line):
    if ((line[0] == '"' and line[-1] == '"') or (line[0] == "'" and line[-1] == "'")):
      if line[0] == "'":
        line = line[1:-1]
      if line and line[0] == "\"":
        line = line[1:-1]
    return line

  @staticmethod
  def _section(line):
    line  = INI._dequote(line)
    colon = line.find(':')
    if colon >= 0:   # if the line contains a descriptor, delete it from section
      line = line[0:colon].strip()
    return line

  @staticmethod
  def _eval(ini, line):
    res = ""
    if "$(" in line:
      if ")" not in line:
        raise MalformedVariableError("Variable doesn't contain a closing paren ')'", line)
      ons = line.find('$(') + 2
      end = line.find(')', ons)
      if ons == end:
        raise MalformedVariableError("Empty variable: $()", line)
      res = line[ons:end].replace("'", "")
      res = res.replace("\"", "")
      if "." in res:
        sec, var = res.split('.', 1)
        old = "$({}.{})".format(sec, var)
      else:
        sec = "default"
        var = res
        old = "$({})".format(var)
      if ini.get(sec) == None: 
        raise MalformedVariableError("Undefined variable: $({}.{})".format(sec, var), line)
      if ini.get(sec).get(var) == None:
        raise MalformedVariableError("Undefined variable: $({}.{})".format(sec, var), line)
      new  = ini.get(sec).get(var)
      if new == None or len(new) < 1:
        raise MalformedVariableError("Undefined variable: $({}.{})".format(sec, var), line)
      line = line.replace(old, new)
    return line  
  
  @staticmethod
  def read(name,sep="="):
    """
    Read an INI style configuration file and return a dict of arrays.

    
    Given a config file formatted like this:

    # Admin user account
    username  = 'awi\prcLCCVMWare'

    #
    # Obfuscated Password account
    password  =  PASSWORD('0KOacbUxehNxkRa8JKUrCQCJ6CqTBvuzXSpqzzPYu+')

    ##
    ## An array of all available vcenters
    ## Required by snchk (snap check)
    ##
    ['vcenters']
      haha.joedog.org
      papa.joedog.org
      mama.joedog.org
      lala.joedog.org   # HA HA
      dada.joedog.org   # Disaster recovery

    ['pirates']
      pitcher      = Joe Musgrove
      catcher      = Jacob Stallings
      first base   = Josh Bell
      second base  = Adam Frazier
      third base   = Colin Moran
      short stop   = Kevin Newman
      left field   = Bryan Reynolds
      center field = Starling Marte
      right field  = Gregory Polanco


    ini = INI.read('config.conf', sep='=')
    print(ini['default']['username'])
    print(ini['default']['password'])
    for server in ini['vcenters']:
      print(server)
    for position in ini['pirates']:
      print("%-10s\t%s" % (position.title(), ini['pirates'][position])) 
    
    NOTE: Items at the top of the file are in an implicit section called 'default'
    They are referenced in the dict like this: ini['default']['username'] Itesm in 
    each ensuring section are referenced by the explicit section name. ini['pirates']
    matches the ['pirates'] section header in the file.

    If the section entries contain a separator (in this case '='), then the parser
    splits each entry into key/value pairs. If the entries don't contain a separator,
    then the parser returns a list for the section. 

    :param name:  String - the path to an INI formatted config file
    :param sep:   Character - a key/value separator for entry lines
    :return:      dictionary
    """
    ini     = {}
    ptr     = ini
    section = None
    section = 'default'
    ptr     = ini[section] = ini.get(section, {})
    regex   = re.compile(r'^\[([^\]]*)\]$|^([^=]+)(=(.*))?$', re.IGNORECASE)
    with open(name, 'r') as f:
      content = f.readlines()

      for line in content:
        line     = line.replace('\n','')
        location = line.find('#')
        if location >= 0:   # if the line has no comment, location is -1
          line = line[0:location].strip()
        line = INI._eval(ini, line.strip()) # variable evaluation $(section.name)
        
        if not line or re.match(r'^\s*[;#]', line):
          # Emptiness, more or less, 
          # It's just a change in me, 
          # Something in my memory...
          continue

        match = regex.match(line)
        if not match:
          continue
         
        if match.group(1):
          section = INI._section(match.group(1))
          continue

        equals = line.find(sep)
        if equals >= 0: 
          if section not in ini:
            ptr = ini[section] = ini.get(section, {})
          arr = line.split(sep, 1)
          arr[0] = INI._dequote(arr[0].strip())
          arr[1] = INI._dequote(arr[1].strip())
          ini[section][arr[0]] = arr[1]
        else: 
          if section not in ini:
            ptr = ini[section] = ini.get(section, [])
          line = line.strip() 
          ini[section].append(line)
    return ini

  @staticmethod
  def exists(name):
    return os.path.exists(name)

class Block(object):
  """
  Block - Reads and parses an logrotatestyle configuration file. The parser honors UNIX style
  hash (#) comments and it trims leading and trailing white space. 

  A block-style configuration file contains global variables in key-value format and blocks of 
  information set within parenthesis. A typical file looks like this:

  verbose = true
  debug   = false

  labas001.joedog.org {
    cmd1 = service puppet stop
    cmd2 = rm -f /var/lib/puppet/state/agent_catalog_run.lock
    cmd3 = service puppet start
  }

  # Example implementation:

  cfg = Block.read("update.conf")
  for server, cmds in sorted(cfg.items()):
    print(server)
    rpc = SSH(server, cfg.get('default').get('username'), cfg.get('default').get('password'))
    for key in sorted(cmds):
      if key.startswith("cmd"):
        out = rpc.run("{}".format(cmds[key]))
        if out:
          print("%s:%s" % (server, out.strip()))

  """
  def read(name,sep="="):
    res = {}
    fh  = None
    sc  = None
    try:
      fh = open(name)
      for line in fh:
        line = line.strip()
        lc   = line.find("#")
        ns   = line.find("{")
        ne   = line.find("}")
        eq   = line.find(sep)
        if lc == 0:
          # this is a block comment
          continue
        if lc >= 0:
          # this is an inline comment
          line = line[0:lc].strip()
        if ns > -1:
          # this is a section declaration
          sc = line[0:ns].strip()
        if ne > -1:
          # end of section
          sc = None
        if sc != None and eq > -1:
          # section elements; assignment block
          if res.get(sc) == None:
            res[sc] = {}
          arr = line.split(sep, 1) # one split yields two parts
          res[sc][arr[0].strip()] = arr[1].strip()
        if sc != None and ns == -1 and eq == -1:
          # section elements; list block (no assignment)
          if res.get(sc) == None:
            res[sc] = []
          res[sc].append(line.strip())
        if sc == None and eq > -1:
          # global section - variables set at the top of the file
          if res.get("default") == None:
            res['default'] = {}
          arr = line.split(sep, 1)
          res['default'][arr[0].strip()] = arr[1].strip()
    except IOError:
      print("File not accessible: %s" % conf)
      return None
    finally:
      if not fh == None:
        fh.close()
    return res

  @staticmethod
  def exists(name):
    return os.path.exists(name)



