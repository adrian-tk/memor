#!/usr/bin/env python3

import re
import cli_parser
import logging
logging.basicConfig(level=logging.DEBUG)

desired_val="666" #default value, if no parameter is given
MAX_CHAR=10000           #maximum searched output in char

#parsing command line arguments
p = cli_parser.ArgPar()
args = p.parser.parse_args()
#when command line arg is "-v" set loglevel to INFO
if args.verbose: logging.getLogger().setLevel(logging.INFO)
if args.loglevel!=None:    
    logl= (getattr(logging, args.loglevel))
    logging.getLogger().setLevel(logl)
logging.debug (f"loglevel is set to: {logging.getLogger().level}")
logging.debug(f"Command line arguments: {args}")
   
if args.val !=None: desired_val=args.val

def search_words(num: str):
    dct=open("srt_dict.txt", "r")
    ptrn = f"^{num} "
    words=""
    for word in dct:
        if re.search(ptrn, word) and len(words)<MAX_CHAR:
            word=word.split()[1] #get second element
            words+=(word+", ")
    dct.close()
    words=words[:-2] #remove ", " from words
    return words
    
if __name__=="__main__":
    words=search_words(str(desired_val))
    print(words)

