#!/usr/bin/env python

from modules.Statistics import Statistics
from modules.filler import poll
import sys,os
import time
import argparse

def doArgs(argList, name):
    parser = argparse.ArgumentParser(description=name)

    parser.add_argument('-v', "--verbose", action="store_true", help="Enable verbose debugging", default=False)
    parser.add_argument('--input', action="store", dest="inputFn", type=str, help="Input file name", required=True)
    parser.add_argument('--output', action="store", dest="outputFn", type=str, help="Output file name", required=True)
    parser.add_argument('--nb', action="store", dest="number", type=str, help="How many lines to generate", required=True)

    return parser.parse_args(argList)

def main():
    progName = "Excel Random Datasets"
    args = doArgs(sys.argv[1:], progName)

    verbose = args.verbose
    inputFn = args.inputFn
    outputFn = args.outputFn
    how_many = int(args.number)

    startTime = float(time.time())

    if not os.path.isfile(inputFn):
        print ("Aliments file doesn't exist, exiting")
        return
    
    if not os.path.isfile(outputFn):
        print ("Sondage file doesn't exist, exiting")
        return

    try:
        poll(how_many)
        s = Statistics()
        s.show_graph() # 10 the first time because past sheet loaded (6+4=10 aliments)
        print(s.most_chosen_categories_tostring())

    except Exception as err:
        print("lol bruh")
        print(err)

    print ("Job done in %0.4f seconds" % (time.time() - startTime))
    return

if __name__ == '__main__':
    sys.argv = ["main.py","--input","Aliments.xlsx","--output","Sondage.xlsx","--nb","100"]
    main()
    os.system("pause")
    