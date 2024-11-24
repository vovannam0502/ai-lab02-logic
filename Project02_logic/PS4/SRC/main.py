import os
from functions import *

def main():
    src_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(src_dir, 'input')
    output_path = os.path.join(src_dir, 'output')

    os.makedirs(output_path, exist_ok=True)
    inputfiles = os.listdir(input_path)

    for filename in inputfiles:
        input_file = os.path.join(input_path, filename)
        output_file = os.path.join(output_path, filename.replace('input', 'output'))

        alpha, KB = read_file(input_file) # Đọc dữ liệu từ file input
        result, isTrue = PL_resolution(KB, alpha) # PL-Resolution
        write_file(result, isTrue, output_file) # Ghi kết quả ra file output

        print(f'Finished resolving {filename}')

if __name__ == '__main__':
    main()