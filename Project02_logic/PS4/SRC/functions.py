# Hàm đọc các dòng từ file input
# Hàm trả về list các literal trong mệnh đề
def split_and_filter(line):
    return [literal for literal in line.split() if literal != 'OR']

# Hàm đọc dữ liệu từ file input
# Hàm trả về alpha và KB
def read_file(filename):
    with open(filename, 'r') as f:
        data = [line.strip() for line in f]

    alpha = split_and_filter(data[0]) # Dòng đầu tiên

    size = int(data[1]) # Số mệnh đề trong KB
    KB = [split_and_filter(data[2 + i]) for i in range(size)]

    return alpha, KB

# Hàm ghi kết quả ra file output
# Hàm ghi số lượng mệnh đề trong mỗi vòng lặp, các mệnh đề trong vòng lặp tương ứng và kết quả hợp giải
def write_file(result, isTrue, filename):
    with open(filename, 'w') as f:
        for i in result:
            f.write(str(len(i)) + '\n') # Ghi số lượng mệnh đề trong mỗi vòng lặp  

            # Ghi từng mệnh đề trong mỗi vòng lặp
            for clause in i:
                clause_str = ' OR '.join(clause)
                f.write(clause_str + '\n')

        f.write('YES' if isTrue else 'NO') # Ghi kết quả hợp giải

# Hàm phủ định một literal, trả về literal phủ định
def negate_literal(literal):
    return literal[1:] if literal.startswith('-') else '-' + literal

# Hàm phủ định một mệnh đề, trả về phủ định của mệnh đề đó
def negate_clause(clause):
    negate_claused = [[negate_literal(literal)] for literal in clause]
    return standard_CNF(negate_claused)

# Hàm loại bỏ mệnh đề có dạng (A or B or -B) hay không
def remove_complementary(clauses):
    result = []
    for clause in clauses:
        # Kiểm tra xem clause có chứa literal và phủ định của nó không
        if not any(negate_literal(literal) in clause for literal in clause):
            result.append(clause)
    return result

# Hàm loại bỏ các mệnh đề trùng lặp, các mệnh đề (A or True)
def remove_redundant_clauses(clauses):
    result = []
    for clause in clauses:
        is_redundant = False
        for existing_clause in result:
            # Kiểm tra clause có phải là con của existing_clause
            if all(literal in existing_clause for literal in clause):
                is_redundant = True
                break
        if not is_redundant:
            result.append(clause)
    return result

# Hàm loại bỏ các literal trùng lặp, sắp xếp theo thứ tự bảng chữ cái
def standard_clause(clause):
    # Loại bỏ các literal trùng lặp
    clause = list(set(clause))

    sorted_clause = sorted(clause, key=lambda x: (x.lstrip('-'), x.startswith('-')))
    return sorted_clause

# Hàm chuẩn hóa mệnh đề thành dạng CNF
def standard_CNF(clauses):
    std_cnf = []
    product_all = list(product_helper(clauses))
    for i in product_all:
        std_clause = standard_clause(i)
        if std_clause not in std_cnf:
            std_cnf.append(std_clause)
            
    std_cnf.sort(key=len)
    std_cnf = remove_redundant_clauses(std_cnf)
    std_cnf = remove_complementary(std_cnf)
    return std_cnf

# Hàm hợp giải hai mệnh đề
def resolve(clause1, clause2):
    resolvents = []
    for literal in clause1:
        neg_literal = negate_literal(literal)
        if neg_literal in clause2:
            # Hợp giải hai mệnh đề
            new_clause = [x for x in clause1 if x != literal] + [y for y in clause2 if y != neg_literal]
            new_clause = standard_clause(new_clause)
            if new_clause not in resolvents:
                resolvents.append(new_clause)
                
    resolvents = remove_redundant_clauses(resolvents)
    resolvents = remove_complementary(resolvents)
    return resolvents

# Thuật toán PL-Resolution
def PL_resolution(KB, alpha):
    clauses = KB[:]

    # Thêm mệnh đề phủ định của alpha vào KB
    negated_alpha = negate_clause(alpha)
    for literal in negated_alpha:
        if literal not in clauses:
            clauses.append(literal)

    result = []
    while True:
        # Lấy ra tất cả các cặp mệnh đề
        clause_pairs = combinations_helper(len(clauses))
        new_clauses = []

        # Hợp giải từng cặp mệnh đề
        for pair in clause_pairs:
            clause1 = clauses[pair[0]]
            clause2 = clauses[pair[1]]
            resolvents = resolve(clause1, clause2)
            for resolvent in resolvents:
                if resolvent == []:  # Phát hiện mệnh đề rỗng, trả về True
                    new_clauses.append(['{}'])
                    # print(f'{clause1} + {clause2} => {resolvent}')
                    result.append(new_clauses)
                    return result, True
                # Nếu mệnh đề mới không trùng với các mệnh đề đã có
                if resolvent not in new_clauses and resolvent not in clauses:
                    new_clauses.append(resolvent)
                    # print(f'{clause1} + {clause2} => {resolvent}')

        # Các mệnh đề mới trong vòng lặp này
        result.append(new_clauses)

        if not new_clauses:  # Nếu không tạo ra thêm mệnh đề, trả về False
            return result, False

        # Thêm các mệnh đề mới vào KB, tiếp tục hợp giải
        for clause in new_clauses:
            if clause not in clauses:
                clauses.append(clause)

# Hàm tạo tất cả các kết hợp của các mệnh đề
def product_helper(clauses):
    result = [[]]
    for clause in clauses:
        result = [x + [y] for x in result for y in clause]
    return result

# Hàm tạo tất cả các kết hợp của các cặp chỉ số
def combinations_helper(n):
    result = []
    for i in range(n):
        for j in range(i + 1, n):
            result.append([i, j])
    return result