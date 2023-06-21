
#  #parsing command line arguments
#import logging
#p = cli_parser.ArgPar()
#args = p.parser.parse_args()
##when command line arg is "-v" set loglevel to INFO
#if args.verbose: logging.getLogger().setLevel(logging.INFO)
#if args.loglevel!=None: 
#    logl= (getattr(logging, args.loglevel))
#    logging.getLogger().setLevel(logl)
#logging.debug (f"loglevel is set to: {logging.getLogger().level}")
#logging.debug(f"Command line arguments: {args}")
#
#if args.first !=None: somevalue=args.hostname
 
import argparse
class ArgPar:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Description")
        self.parser.add_argument('-v', '--verbose', action="store_true", dest="verbose", default=False,
            help="set log level to info. Overrided by --log.")
        self.parser.add_argument('--log', action="store", dest="loglevel",
            help="set loglevel to desired value.",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.parser.add_argument('-a', '--val', action="store", dest="val",
            help="value to find ie. 034")
                
        #dont use --log and -v similtaneously
        if self.parser.parse_args().loglevel != None: 
            self.parser.parse_args().verbose = False

