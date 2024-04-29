import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

# apply multiindex do dfs
def get_setting(value):
    if "pretsa" in value:
        if "K_4" in value:
            return "weak"
        elif "K_16" in value:
            return "average"
        elif "K_64" in value:
            return "strong"
        else:
            print("no setting pretsa", value)
    elif "TLKC" in value:
        if "L_2" in value:
            return "weak"
        elif "L_4" in value:
            return "average"
        elif "L_6" in value:
            return "strong"
        else:
            print("no setting tlkc", value)
    elif "pripel" in value:
        if "epsilon_1.5" in value:
            return "weak"
        elif "epsilon_1.0" in value:
            return "average"
        elif "epsilon_0.5" in value:
            return "strong"
        else:
            print("no setting pripel", value)
    else:
        print("no setting algo", value)

def get_logsize(value):
    if "_1000_" in value:
        return "1000"
    elif "_5000_" in value:
        return "5000"
    else:
        print('no logsize', value)

def get_bktype(value):
    if "multiset" in value:
        return "multiset"
    elif "set" in value:
        return "set"
    elif "relative" in value:
        return "relative"
    elif "sequence" in value:
        return "sequence"
    else:
        print("no bkt", value)

def get_algo(value):
    if "XORANDLOOPSKIP2" in value:
        return "XOR+AND+LOOP+SKIP2"
    elif "XORANDLOOPSKIP1" in value:
        return "XOR+AND+LOOP+SKIP1"
    elif "XORANDLOOP2" in value:
        return "XOR+AND+LOOP2"
    elif "XORANDLOOP1" in value:
        return "XOR+AND+LOOP1"
    elif "XORAND2" in value:
        return "XOR+AND2"
    elif "XORAND1" in value:
        return "XOR+AND1"
    elif "XOR2" in value:
        return "XOR2"
    elif "XOR1" in value:
        return "XOR1"
    else:
        print("no algo complexity", value)

def print_multiindex_structure(index):
    # Determine the maximum width for each level
    max_widths = [0] * index.nlevels
    for idx in index:
        for i, value in enumerate(idx):
            max_widths[i] = max(max_widths[i], len(str(value)))

    # Track the last seen values for each index level
    last_values = [""] * index.nlevels
    output_lines = []

    # Iterate over each index and generate the output with fixed-width columns
    for idx in index:
        line = []
        for i, value in enumerate(idx):
            if value != last_values[i]:  # If value has changed, format it
                empty_space = " " * max_widths[i]
                formatted_value = str(value).ljust(max_widths[i])
                line.append(formatted_value)
                last_values[i] = value
            else:  # Otherwise, leave it blank with the same fixed width
                empty_space = " " * max_widths[i]
                line.append(empty_space)
        output_lines.append("   ".join(line))  # Use a consistent separator for readability

    return output_lines