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

        # Đọc dữ liệu từ file input
        alpha, KB = read_file(input_file)

        # PL-Resolution
        result, check = PL_resolution(KB, alpha)

        # Ghi kết quả ra file output
        write_file(result, check, output_file)

if __name__ == '__main__':
    main()