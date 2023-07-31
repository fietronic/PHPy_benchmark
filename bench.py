import os
import sys
import time
import hashlib
import random

if len(sys.argv) >= 4:
    dir_name = sys.argv[1]
    tmp_path = sys.argv[2].strip("'")
    test_time = int(sys.argv[3])
    print(f"bench.py (dir_name) (tmp_path) (test_time): {dir_name} {tmp_path} {test_time}")
else:
    print("bench.py error: dir_name tmp_path test_time")
    quit()

def sum_of_natural_numbers_test():
    n = 1000
    sum = 0
    for i in range(1, n + 1):
        sum += i

def fancy_sum_of_natural_numbers_test():
    n = 1000
    _ = sum(range(1, n+1))

def md5_hash_calculation_test():
    data = b"Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    for _ in range(1000):
        hashlib.md5(data).hexdigest()

def random_number_generation_test():
    for _ in range(1000):
        random.randint(0, 100)

def string_concatenation_test():
    result = ""
    for _ in range(1000):
        result += "Lorem ipsum dolor sit amet, "

def matrix_multiplication_test():
    size = 100  # Half the number of iterations compared to others
    matrix1 = [[i + j for j in range(size)] for i in range(size)]
    matrix2 = [[i - j for j in range(size)] for i in range(size)]
    result = [[0 for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(size):
            for k in range(size):
                result[i][j] += matrix1[i][k] * matrix2[k][j]

def file_io_test():
    file_path = tmp_path+"py_benchmark_test.txt"

    content = "f5*8sj!@%uKgP#T9Q&cA+d2^vhZ6bG9qU*rLMEnoV!xItTzNh%O^fqJjR&U*Lo8*mSdMvWJkTjz%hx9YypS3ecmqLnqehOM4vMK5nNvBXUzNz5#3QVy3K6u0Ad8p7xhWp2z9R0QiwzI0sXzCjaZrnojbfXnGf^&3M!J3+QGRM2FaZGkWi!PZJEM1bWVuDQb7PA5gJPd1#jn+X9QGv"
    with open(file_path, "w") as file:
        file.write(content)
    with open(file_path, "r") as file:
        file.read()


def associative_array_manipulation_test():
    data = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
    }

    # Reverse the array
    reversed_data = {}
    keys = list(data.keys())
    for i in range(len(keys) - 1, -1, -1):
        reversed_data[keys[i]] = data[keys[i]]

    # Sort the array (bubble sort)
    sorted_data = data.copy()
    length = len(sorted_data)
    for i in range(length - 1):
        for j in range(length - i - 1):
            if sorted_data[keys[j]] > sorted_data[keys[j + 1]]:
                temp = sorted_data[keys[j]]
                sorted_data[keys[j]] = sorted_data[keys[j + 1]]
                sorted_data[keys[j + 1]] = temp

def run_benchmark(test_function):
    start_time = time.time()
    end_time = start_time + test_time #test duration

    iterations = 0
    while time.time() < end_time:
        test_function()
        iterations += 1

    return iterations

outfile = dir_name + "/python_benchmark.txt"
# Run the benchmarks and save results to a file
with open(outfile, "w") as file:
    file.write(f"Sum of N Natural Numbers Test: {run_benchmark(sum_of_natural_numbers_test)}\n")
    file.write(f"Fancy Sum of N Natural Numbers Test: {run_benchmark(fancy_sum_of_natural_numbers_test)}\n")
    file.write(f"MD5 Hash Calculation Test: {run_benchmark(md5_hash_calculation_test)}\n")
    file.write(f"Random Number Generation Test: {run_benchmark(random_number_generation_test)}\n")
    file.write(f"String Concatenation Test: {run_benchmark(string_concatenation_test)}\n")
    file.write(f"Matrix Multiplication Test: {run_benchmark(matrix_multiplication_test)}\n")
    file.write(f"File I/O Operations Test: {run_benchmark(file_io_test)}\n")
    file.write(f"Associative Array Manipulation Test: {run_benchmark(associative_array_manipulation_test)}\n")


os.remove(os.path.join(tmp_path, "py_benchmark_test.txt"))