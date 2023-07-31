import os
import time
import matplotlib.pyplot as plt
import re
import matplotlib.ticker as ticker
import sys
import platform
import psutil

if len(sys.argv) >= 2:
    dir_name = sys.argv[1]

    print(f"plot3.py (dir_name): {dir_name}")
else:
    print("plot3.py error: dir_name")
    quit()


# Function to read data from a file and extract test names and iterations
def read_benchmark_results(file_path):
    test_names = []
    iterations = []
    with open(file_path, "r") as file:
        for line in file:
            test_name, iteration = line.strip().split(": ")
            test_names.append(test_name)
            iterations.append(int(iteration))
    return test_names, iterations

# Function to clean up the test name for use as a label
def clean_test_name(test_name):
    return re.sub(r'\W+', '', test_name)

# Function to format large numbers into more readable forms
def format_large_numbers(x, pos):
    if x >= 1e6:
        return f"{int(x/1e6)}M"
    elif x >= 1e3:
        return f"{int(x/1e3)}K"
    else:
        return str(int(x))

# Function to create a bar chart for a specific test
def create_single_bar_chart(test_name, php_iteration, python_iteration, output_directory, i):
    test_name_cleaned = clean_test_name(test_name)
    bar_width = 0.4
    index = [0, 1]

    plt.barh(index, [php_iteration, python_iteration], color=['#787cb5', '#3EB049'], height=bar_width)
    plt.yticks(index, ['PHP', 'Python'])
    
    # Set the custom formatting for y-axis tick labels
    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(format_large_numbers))
    
    plt.xlabel('Iterations')
    plt.ylabel('Language')
    plt.title(f'{test_name} Benchmark Results')
    plt.tight_layout()

    # Add operating system and hardware information
    os_info = platform.platform()
    cpu_info = f"{psutil.cpu_count(logical=False)} cores, {psutil.cpu_freq().max:.2f} MHz max freq"
    memory_info = f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB RAM"
    sys_info_text = f"OS: {os_info}, CPU: {cpu_info}, RAM: {memory_info}"
    
    plt.figtext(0.5, 0.01, sys_info_text, ha='center', fontsize=8)

    # Create the directory for benchmark results
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    timestamp = int(time.time())  # Get the current Unix timestamp
    file_name = os.path.join(output_directory, f'{i}_{test_name_cleaned.lower()}_benchmark.png')
    
    plt.savefig(file_name)
    plt.close()  # Close the figure to release memory
    # Uncomment the line below if you want to display the plots as well
    # plt.show()

# Read data from PHP and Python benchmark files
php_test_names, php_iterations = read_benchmark_results(dir_name+"/php_benchmark.txt")
python_test_names, python_iterations = read_benchmark_results(dir_name+"/python_benchmark.txt")

# Create individual bar charts for each test
for i, test_name in enumerate(php_test_names):
    if test_name in python_test_names:
        php_index = php_test_names.index(test_name)
        python_index = python_test_names.index(test_name)
        create_single_bar_chart(test_name, php_iterations[php_index], python_iterations[python_index], dir_name, i)
