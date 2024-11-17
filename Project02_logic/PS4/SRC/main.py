import os
from functions import *

def readInput(filename):
    data = []
    with open(filename, 'r') as f:
        data = f.read().splitlines()

    alpha = [data[0]]
    query = []
    for cnf in alpha:
        clause = cnf.split()
        clause = list(filter(lambda x: x != 'OR', clause))
        query.append(clause)

    KB = initKnowledgeBase()
    KB_size = int(data[1])
    KB_string = data[2:]
    for cnf in KB_string:
        clause = cnf.split()
        clause = list(filter(lambda x: x != 'OR', clause))
        addClause(KB, clause)

    return KB, query


def writeOutput(result, check, filename):
    with open(filename, 'w') as f:
        for loop_res in result:
            f.write(str(len(loop_res)) + '\n')
            for clause in loop_res:
                string = ''
                for c in clause:
                    string += c
                    if c != clause[-1]:
                        string += ' OR '
                f.write(string + '\n')
        if check:
            f.write('YES')
        else:
            f.write('NO')

INPUT_DIR = '../IntroAI-Lab02-Logic/Project02_logic/PS4/SRC/input/'
OUTPUT_DIR = '../IntroAI-Lab02-Logic/Project02_logic/PS4/SRC/output/'

inputs = os.listdir(INPUT_DIR)
for filename in inputs:
    input_filename = INPUT_DIR + filename
    KB, query = readInput(input_filename)

    result, check = PLResolution(KB, query)
    
    output_filename = OUTPUT_DIR + 'output' + filename[6:]
    writeOutput(result, check, output_filename)