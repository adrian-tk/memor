#!/usr/bin/env python3

#You can dump a dict from aspell using:
#aspell -d pl dump master | aspell -l pl expand > pldict.txt
import sqlite3
import os
import logging
logging.basicConfig(level=logging.DEBUG)
import argparse

RAW_DICT="pldict.txt"

class ArgPar:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="Dictionary parser")
        self.parser = argparse.ArgumentParser(description="Preparing dictionary for using")
        self.parser.add_argument('-v', '--verbose', action="store_true", dest="verbose", default=False,
            help="set log level to info. Overrided by --log.")
        self.parser.add_argument('--log', action="store", dest="loglevel",
            help="set loglevel to desired value.",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
#        self.parser.add_argument('-a', '--val', action="store", dest="val",
#            help="value to find ie. 034")
        self.parser.add_argument('dict_file', type=argparse.FileType('r'),
                                 nargs='?', metavar="DICTIONARY_FILE")
                
        self.parser.add_argument('-a', '--aspell', action="store", dest="aspell",
            help="dump a aspell dictionary", metavar="COUNTRY_CODE")

        #dont use --log and -v similtaneously
        if self.parser.parse_args().loglevel != None: 
            self.parser.parse_args().verbose = False

        if self.parser.parse_args().aspell is not None and self.parser.parse_args().dict_file is not None:
            logging.critical(f"Can't use at this same time aspell and dictionary file")
            exit()
            



#parsing command line arguments
p = ArgPar()
args = p.parser.parse_args()
#when command line arg is "-v" set loglevel to INFO
if args.verbose: logging.getLogger().setLevel(logging.INFO)
if args.loglevel!=None:
    logl= (getattr(logging, args.loglevel))
    logging.getLogger().setLevel(logl)
logging.debug (f"prep_dict: loglevel is set to: {logging.getLogger().level}")
logging.debug(f"prep_dict: Command line arguments: {args}")
raw_dictionary=""
if args.dict_file is not None:
    raw_dictionary=args.dict_file.name
    logging.info(f'prep_dict: dictionary file {str(args.dict_file.name)} '\
               'is given in command line')
else:
    raw_dictionary=RAW_DICT
    logging.info(f'prep_dict: default dictionary file: {RAW_DICT}')

def next_chr(word, pos):
    if pos < len(word)-1:
        return word[pos+1]
    else:
        return "0"

def prev_chr(word, pos):
    if pos > 0:
        return word[pos-1]
    else:
        return "0"

def calc_val(word):
    number = ""
    position=0
    for position in range(len(word)):
        match word[position]:
            case ("s"|"S"):
                if next_chr(word, position)!="z" and \
                   next_chr(word, position)!="i":
                    number+="0"
            case ("z"|"Z"):
                if prev_chr(word, position)!="r" and \
                   prev_chr(word, position)!="R" and \
                   prev_chr(word, position)!="s" and \
                   prev_chr(word, position)!="S" and \
                   prev_chr(word, position)!="i" and \
                   prev_chr(word, position)!="I" and \
                   prev_chr(word, position)!="c" and \
                   prev_chr(word, position)!="C":
                    number=number
            case ("d"|"t"|"D"|"T"):
                number+="1"
            case ("n"|"N"):
                number+="2"
            case ("m"|"M"):
                number+="3"
            case ("r"|"R"):
                if next_chr(word, position)!="z":
                    number+="4"
            case ("l"|"L"):
                number+="5"
            case ("j"|"J"):
                number+="6"
            case ("k"|"g"|"K"|"G"):
                number+="7"
            case ("f"|"w"|"F"|"W"):
                number+="8"
            case ("p"|"b"|"P"|"B"):
                number+="9"
        position+=1
    return number

def sort_dict(input_dict, output_dict):
    unsrt_dict = open(input_dict, "r")
    srt_dict = open(output_dict, "w")
    contents = unsrt_dict.readlines()
    contents.sort()
    srt_dict.writelines(contents)
    unsrt_dict.close()
    srt_dict.close()


def add_val(input_dict, output_dict):
    org_dict = open(input_dict, "r")
    val_dict = open(output_dict, "w")
    line=org_dict.readline()
    i=0 #TODO big int?
    while line: #and i<1000000:
        number = calc_val(line)
        newline = number + " " + line
        if i%100000==0:  #print dot for defined lines
            logging.debug(f"calculated {i} lines")
        val_dict.write(newline)
        line=org_dict.readline()
        i = i+1
    logging.info(f"calculated {i} lines in total")
    org_dict.close()
    val_dict.close()

def leave_first(input_dict, output_dict):
    in_dict = open(input_dict, "r")
    out_dict = open(output_dict, "w")
    line=in_dict.readline()
    i=0 #TODO big int?
    while line: 
        newline = line.split()[0]
        if i%100000==0:  #print dot for defined lines
            logging.debug(f"cleaned {i} lines")
        out_dict.write(newline+"\n")
        line=in_dict.readline()
        i = i+1
    logging.info(f"cleaned {i} lines in total")
    in_dict.close()
    out_dict.close()

def import_aspell(code):
    logging.info(f"prep_dict: dumping aspell dictionary for {code} country code")
    os.system(f"aspell -d {code} dump master | aspell -l {code} expand > aspell_dict.txt")
    


if args.aspell is not None:
    import_aspell("pl")
    raw_dictionary="aspell_dict.txt"   
leave_first(raw_dictionary, "one_dict.txt")
add_val("one_dict.txt", "val_dict.txt")
sort_dict("val_dict.txt", "srt_dict.txt")
