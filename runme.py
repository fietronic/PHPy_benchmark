import os
import subprocess
import time
import shlex  # safely escape command-line arguments
import re
import sys


def get_php_path():
    try:
        # Try using 'where' command on Windows
        result = subprocess.run(['where', 'php'], capture_output=True, text=True, check=True)
        php_path = result.stdout.strip()
        if php_path:
            return php_path
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    try:
        # Try using 'which' command on Unix-like systems (Linux, macOS)
        result = subprocess.run(['which', 'php'], capture_output=True, text=True, check=True)
        php_path = result.stdout.strip()
        if php_path:
            return php_path
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # Fallback: Search for PHP using the regex pattern in the PATH directories
    php_pattern = re.compile(r"^php(?:\d+(?:\.\d+)?)?(?:\.exe)?$")  # Pattern to match "php" followed by digits and possibly a dot and more digits, or "php.exe"
    paths = os.environ.get("PATH", "").split(os.pathsep)

    for path in paths:
        for entry in os.listdir(path):
            if php_pattern.match(entry):
                php_path = os.path.join(path, entry)
                if os.path.isfile(php_path) and os.access(php_path, os.X_OK):
                    return php_path

    return None  # PHP executable not found


def create_directory():
    # Get the current Unix timestamp
    unixtime = int(time.time())
    # Create the directory name in the required format
    dir_name = f"result_{unixtime}"
    
    # Create the directory
    os.mkdir(dir_name)
    
    return dir_name


def get_valid_path():
    while True:
        path = input("Path for I/O test (many writes): ")
        path = os.path.normpath(path)  # Normalize the path to handle slashes for the OS
        if not path.endswith(os.sep):  # Add a trailing slash if it's missing
            path += os.sep

        if os.path.exists(path) and os.path.isdir(path):
            return path
        else:
            print("Path does not exist or is not a directory. Please enter a valid directory path.")

def get_valid_time():
    while True:
        testtime = int(input("Seconds for each test: "))
        if testtime > 0:
            return str(testtime)
        else:
            print("Positive Integer Please.")


def run_command(command):
    # Run the command in the shell and wait for completion
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    php_path = get_php_path()
    if php_path is None:
        print ("Can't find PHP")
        quit()
    
    python_path = os.path.abspath(sys.executable)
    # Create the directory
    dir_name = create_directory()

    # Get the user-entered directory path
    tmp_path = get_valid_path()
    print(tmp_path)

    test_time = get_valid_time()

    # Run the PHP script
    php_command = f"{php_path} bench.php {shlex.quote(dir_name)} {shlex.quote(tmp_path)} {shlex.quote(test_time)}"
    print(php_command)
    run_command(php_command)

    # Run the Python script
    python_command = f"{python_path} bench.py {shlex.quote(dir_name)} {shlex.quote(tmp_path)} {shlex.quote(test_time)}"
    print(python_command)
    run_command(python_command)

    # Run the third Python script
    plot_command = f"{python_path} plot3.py {shlex.quote(dir_name)}"
    print(plot_command)
    run_command(plot_command)

    print("All commands executed successfully.")
