#!/usr/bin/env python3

#You can dump a dict from aspell using:
#aspell -d pl dump master | aspell -l pl expand > pldict.txt

RAW_DICT="pldict.txt"

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
                    number+="x"
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
            print(f"converted {i} lines")
        val_dict.write(newline)
        line=org_dict.readline()
        i = i+1
    print(f"converted {i} lines in total")
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
            print(f"converted {i} lines")
        out_dict.write(newline+"\n")
        line=in_dict.readline()
        i = i+1
    print(f"converted {i} lines in total")
    in_dict.close()
    out_dict.close()


leave_first(RAW_DICT, "one_dict.txt")
add_val("one_dict.txt", "val_dict.txt")
sort_dict("val_dict.txt", "srt_dict.txt")

