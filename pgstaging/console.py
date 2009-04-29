## console.py
##
## http://code.activestate.com/recipes/280500/
##
## Author:   James Thiele
## Date:     27 April 2004
## Version:  1.0
## Location: http://www.eskimo.com/~jet/python/examples/cmd/
## Copyright (c) 2004, James Thiele

import os, cmd, readline, sys
import options, commands

class Console(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "pg_staging> "
        self.intro  = "Welcome to pg_staging %s." % options.VERSION        
        self.conffile = None

    ## Command definitions ##
    def do_hist(self, args):
        """Print a list of commands that have been entered"""
        print self._hist

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    ## Command definitions to support Cmd object functionality ##
    def do_EOF(self, args):
        """Exit on system end of file character"""
        return self.do_exit(args)

    def do_shell(self, args):
        """Pass command to a system shell when line begins with '!'"""
        os.system(args)

    def do_config(self, args):
        """ set the configuration file to use """
        if args == "":
            print self.conffile
        else:
            self.set_config(args)

    def do_get(self, args):
        """ get current configuation option value for given database """
        if self.conffile:
            if args != "":
                try:
                    commands.get_config_option(self.conffile, args.split(" "))
                except Exception, e:
                    print e
            else:
                print "Error: get dbname option"
        else:
            print "Error: no config file"

    def do_set(self, args):
        """ set a configuration file option """
        if self.conffile:
            if args != "":
                try:
                    commands.set_config_option(self.conffile, args.split(" "))
                except Exception, e:
                    print e
            else:
                print "Error: set dbname option value"
        else:
            print "Error: no config file"

    def do_verbose(self, args):
        """ toggle verbose on/off """
        options.VERBOSE = not options.VERBOSE
        print "verbose: %s" % str(options.VERBOSE)

    def do_help(self, args):
        """Get help on commands
           'help' or '?' with no arguments prints a list of commands for which help is available
           'help <command>' or '? <command>' gives help on <command>
        """
        ## The only reason to define this method is for the help text in the
        ## doc string
        cmd.Cmd.do_help(self, args)

    ## Override methods in Cmd object ##
    def preloop(self):
        """Initialization before prompting user for commands.
           Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}

    def postloop(self):
        """Take care of any unfinished business.
           Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
        """
        cmd.Cmd.postloop(self)   ## Clean up command completion
        print "Exiting..."

    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
        """
        self._hist += [ line.strip() ]
        return line

    def postcmd(self, stop, line):
        """If you want to stop the console, return something that evaluates to true.
           If you want to do some post command processing, do it here.
        """
        return stop

    def emptyline(self):    
        """Do nothing on empty input line"""
        pass

    def default(self, line):       
        """Called on an input line when the command prefix is not
           recognized.  In that case we refer to
           commands.parse_input_line_and_run_command() function.
        """

        if self.conffile:
            try:
                commands.parse_input_line_and_run_command(self.conffile, line)
            except Exception, e:
                # prints are already managed in commands module
                pass
        else:
            print "Error: no config file"

    def set_config(self, conffile, recheck = True):
        """ set self.conffile  """
        from options import VERBOSE

        # check existence and read ability of config file
        if recheck:
            if VERBOSE:
                print "Checking if config file '%s' exists" % conffile

            if not os.path.exists(conffile):
                print >>sys.stderr, \
                      "Error: '%s' does not exists" % conffile
                return

            if VERBOSE:
                print "Checking if config file '%s' is readable" % conffile

            if not os.access(conffile, os.R_OK):
                print >>sys.stderr, \
                      "Error: Can't read configuration file '%s'" % conffile
                return

        self.conffile = conffile
        if VERBOSE:
            print "Configuration file is:", self.conffile

if __name__ == '__main__':
        console = Console()
        console . cmdloop()
        
