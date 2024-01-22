toolkit helper modules
- cipher - obfuscates text strings
- config - reads data from config files into python data structures
- rpc    - executes remote procedures 
- util   - various helpers


from toolkit.config import Column, Columns, Slurp, INI, Block

# Reads a column formatted config file which may contain hash (#) comments
# The parser strips leading and trailing white space along with new line
# characters.
col  = Column.read("col.conf") 

# Columns - Reads a character separated config file and returns a multidimensional array
# of the colummns in the file. The parser recognizes UNIX style hash (#) comments and it
# trims leading and trailing white space
cols = Columns.read("cols.conf", sep='|')

# INI - Reads and parses an INI style configuration file. The parser honors UNIX style
# hash (#) comments and it trims leading and trailing white space.
ini  = INI.read("cfg.ini", sep='=')

# Block - Reads and parses an logrotatestyle configuration file. The parser honors UNIX style
# hash (#) comments and it trims leading and trailing white space.
#
# A block-style configuration file contains global variables in key-value format and blocks of
# information set within parenthesis. A typical file looks like this:
#
# Example file:
verbose = true
debug   = false

labas001.joedog.org {
  cmd1 = service puppet stop
  cmd2 = rm -f /var/lib/puppet/state/agent_catalog_run.lock
  cmd3 = service puppet start
}

# Example call
cfg = Block.read("block.conf", sep="=")


# Slurp - Reads the whole file (including comments) into a string
s = Slurp.read('filename')




