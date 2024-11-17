import itertools

def initKnowledgeBase():
    return []

def addClause(KB, clause):
    if clause not in KB and not checkComplementary(clause):
        KB.append(clause)

def getNegativeAtom(atom):
    return atom[1:] if atom[0] == '-' else '-' + atom

def getNegativeQuery(query): # Không dùng thư viện itertools.chain
    res = []
    for clause in query:
        new = []
        for atom in clause:
            new.append([getNegativeAtom(atom)])
        res.append(new)

    if len(res) == 1:
        return list(itertools.chain.from_iterable(res))
    else:
        return convertToCNF(res)
    
def checkTrue(clause, list_clauses):
    for c in list_clauses:
        if set(c).issubset(set(clause)):
            return True
    return False

def checkComplementary(clause):
    for atom in clause:
        if getNegativeAtom(atom) in clause:
            return True
    return False

def removeEval(clauses):
    res = []
    for c in clauses:
        if not checkTrue(c, res):
            res.append(c)
    return res

def convertToCNF(clauses):
    res = []
    product_all = list(itertools.product(*clauses))
    for i in product_all:
        new = normClause(list(itertools.chain.from_iterable(list(i))))
        if not checkComplementary(new) and new not in res:
            res.append(new)
    res.sort(key=len)
    res = removeEval(res)
    return res

def normClause(clause):
    # Remove duplicates
    clause = list(dict.fromkeys(clause))

    # Sort by alphabet
    tuple_form = []
    for atom in clause:
        if atom[0] == '-':
            tuple_form.append((atom[1], -1))
        else:
            tuple_form.append((atom[0], 1))
    tuple_form.sort()

    # Rebuild clause
    res = []
    for tup in tuple_form:
        if tup[1] == -1:
            res.append('-' + tup[0])
        else:
            res.append(tup[0])
    return res

def resolve(KB, clause_i, clause_j):
    new_clause = []
    for atom in clause_i:
        neg_atom = getNegativeAtom(atom)
        if neg_atom in clause_j:
            temp_c_i = clause_i.copy()
            temp_c_j = clause_j.copy()
            temp_c_i.remove(atom)
            temp_c_j.remove(neg_atom)
            if not temp_c_i and not temp_c_j:
                new_clause.append(['{}'])
            else:
                clause = temp_c_i + temp_c_j
                clause = normClause(clause)
                if not checkComplementary(clause) and clause not in KB:
                    new_clause.append(clause)
    return new_clause

def PLResolution(KB, query):
    tempKB = KB.copy()

    neg_query = getNegativeQuery(query)
    print(neg_query)
    for neg_atom in neg_query:
        addClause(tempKB, neg_atom)

    result = []
    while True:
        clause_pairs = list(itertools.combinations(range(len(tempKB)), 2))
        
        resolvents = []
        for pair in clause_pairs:
            resolvent = resolve(tempKB, tempKB[pair[0]], tempKB[pair[1]])
            if resolvent and resolvent not in resolvents:
                resolvents.append(resolvent)

        resolvents = list(itertools.chain.from_iterable(resolvents))
        result.append(resolvents)

        if not resolvents:
            return result, False
        else:
            if ['{}'] in resolvents:
                return result, True
            else:
                for res in resolvents:
                    addClause(tempKB, res)