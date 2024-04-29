import subprocess
import re
import os
import shutil


def run_ged(a_value1, a_value2, log_dir):
    # Change current working directory to D:\CalculateGED\
    os.chdir('D:\CalculateGED')

    command = ['ged.bat', a_value1, a_value2]
    subprocess.run(command, stdout=subprocess.PIPE)

    # Move log file to the specified directory
    log_file = f"{a_value1}-{a_value2}.ged.log"
    source = os.path.join('D:\CalculateGED', log_file)  # Source file path
    destination = os.path.join(log_dir, log_file)  # Destination file path
    try:
        shutil.move(source, destination)
    except FileNotFoundError:
        print(f"Error: Cannot find {source}")

    # Change back to the original working directory
    os.chdir(log_dir)


def extract_ged_value(log_file):
    with open(log_file, 'r') as file:
        log_content = file.read()
        match = re.search(r'GED = (\d+\.\d+)', log_content)
        if match:
            return float(match.group(1))
        else:
            return None


def main():
    log_dir = 'D:/CalculateGED/'  # Directory to store log files
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    a_pairs = [('a12', 'a33'), ('a22', 'a12')]  # Add other pairs as needed
    ged_values = {}

    for a_value1, a_value2 in a_pairs:
        run_ged(a_value1, a_value2, log_dir)
        log_file = os.path.join(log_dir, f"{a_value1}-{a_value2}.ged.log")
        ged_value = extract_ged_value(log_file)
        if ged_value is not None:
            ged_values[(a_value1, a_value2)] = ged_value

    # Save GED values to a dictionary
    with open('geds\ged_values.txt', 'w') as file:
        for (a_value1, a_value2), ged_value in ged_values.items():
            file.write(f"{a_value1} - {a_value2}: {ged_value}\n")


if __name__ == "__main__":
    main()
