import os
from functions import *

def main():
    io_path = '../IntroAI-Lab02-Logic/Project02_logic/PS4/SRC/'
    input_path = os.path.join(io_path, 'input/')
    output_path = os.path.join(io_path, 'output/')

    os.makedirs(output_path, exist_ok=True)
    inputfiles = os.listdir(input_path)

    for filename in inputfiles:
        input_file = os.path.join(input_path, filename)
        output_file = os.path.join(output_path, filename.replace('input', 'output'))
        alpha, KB = read_file(input_file) # Đọc dữ liệu từ file input
        result, check = PL_resolution(KB, alpha) # PL-Resolution
        write_file(result, check, output_file) # Ghi kết quả ra file output

if __name__ == '__main__':
    main()