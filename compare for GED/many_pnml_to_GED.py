import subprocess
import re
import os
import shutil
import pandas as pd


def run_ged(a_value1, a_value2, log_dir):
    # Change current working directory to D:\CalculateGED\
    os.chdir('D:\CalculateGED2')

    command = ['ged.bat', a_value1, a_value2]
    subprocess.run(command, stdout=subprocess.PIPE)

    # Move log file to the specified directory
    log_file = f"{a_value1}-{a_value2}.ged.log"
    source = os.path.join('D:\CalculateGED2', log_file)  # Source file path
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
    log_dir = 'D:/CalculateGED2/'  # Directory to store log files
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    #log_paths = ["D:\PPPM_nets\simple\XOR", "D:\PPPM_nets\simple\XORAND", "D:\PPPM_nets\simple\XORANDLOOP", "D:\PPPM_nets\simple\XORANDLOOPSKIP", "D:\PPPM_nets\complex\XOR", "D:\PPPM_nets\complex\XORAND", "D:\PPPM_nets\complex\XORANDLOOP", "D:\PPPM_nets\complex\XORANDLOOPSKIP"]
    #algos = ["pretsacase", "tlkc", "pripel"]
    log_paths = ["D:\PPPM_nets\simple\XOR", "D:\PPPM_nets\simple\XORAND"]
    algos = ["pripel"]
    ged_values = {}

    for path in log_paths:
        for model in algos:
            path_model = os.path.join(path, model)
            files = os.listdir(path_model)
            for file in files:
                if "XOR1_5000_epsilon_1.5" in file or "XORAND1_5000_epsilon_1.5" in file or "XOR1_5000_epsilon_1.0" in file:
                    if "_1000" in file:
                        logzsize = "_1000"
                    if "_5000" in file:
                        logzsize = "_5000"
                    if "simple" in path:
                        if "XORANDLOOPSKIP" in path:
                            base_file = "XORANDLOOPSKIP1" + logzsize
                        elif "XORANDLOOP" in path:
                            base_file = "XORANDLOOP1" + logzsize
                        elif "XORAND" in path:
                            base_file = "XORAND1" + logzsize
                        elif "XOR" in path:
                            base_file = "XOR1" + logzsize
                    elif "complex" in path:
                        if "XORANDLOOPSKIP" in path:
                            base_file = "XORANDLOOPSKIP2" + logzsize
                        elif "XORANDLOOP" in path:
                            base_file = "XORANDLOOP2" + logzsize
                        elif "XORAND" in path:
                            base_file = "XORAND2" + logzsize
                        elif "XOR" in path:
                            base_file = "XOR2" + logzsize

                    # make sure your original pnml file is called XORs and the discovered ones are called XORnr nr=[100,5000], and stored in the same location as CalculateGED
                    #base_file = "XOR+AND+LOOP+SKIP"
                    #other_files = [f"XOR+AND+LOOP+SKIP{nr}" for nr in range(100, 1401, 1300)]
                    other_file = file.replace(".pnml", "")
                    a_pairs = [(base_file, other_file)]
                    #a_pairs = list(zip(other_files[:-1], other_files[1:]))
                    #a_pairs = [(base_file, other_file) for other_file in other_files]

                    #a_pairs = [('a12', 'a33'), ('a22', 'a12')]  # Add other pairs as needed
                    #ged_values = {}

                    for a_value1, a_value2 in a_pairs:
                        print(a_value1, a_value2)
                        run_ged(a_value1, a_value2, log_dir)
                        print(a_value1, a_value2, "Done")
                        log_file = os.path.join(log_dir, f"{a_value1}-{a_value2}.ged.log")
                        ged_value = extract_ged_value(log_file)
                        if ged_value is not None:
                            ged_values[(a_value1, a_value2)] = ged_value

    # Save GED values to a dictionary
    with open('D:\CalculateGED2\geds\geds_txt6.txt', 'w') as file:
        for (a_value1, a_value2), ged_value in ged_values.items():
            file.write(f"{a_value1} - {a_value2}: {ged_value}\n")

    index = pd.MultiIndex.from_tuples(ged_values.keys(), names=['a_value1', 'a_value2'])
    df = pd.DataFrame(list(ged_values.values()), index=index, columns=['ged_value'])
    print(df)
    df.to_csv('D:\CalculateGED2\geds\geds_df6.csv')


if __name__ == "__main__":
    main()
