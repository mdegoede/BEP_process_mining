import subprocess
import re
import os
import shutil
import pandas as pd


def run_ged(a_value1, a_value2, log_dir):
    # Change current working directory to CalculateGED\
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Set the correct working directory
    os.chdir(log_dir)

    command = ['ged.bat', a_value1, a_value2]
    subprocess.run(command, stdout=subprocess.PIPE)

    # Move log file to the specified directory
    log_file = f"{a_value1}-{a_value2}.ged.log"
    source = os.path.join('BEP_process_mining\CalculateGED', log_file)  # Source file path
    destination = os.path.join(log_dir, log_file)  # Destination file path
    try:
        shutil.move(source, destination)
    except:
        none = None

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