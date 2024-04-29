import os
from pm4py.objects.conversion.log import converter as xes_converter
from pm4py.objects.log.importer.xes import importer as xes_importer
import pandas as pd

# Define the directory paths for simple and complex logs
simple_logs_dir = "D:/logs/simple"
complex_logs_dir = "D:/logs/complex"

# Define the different log sizes
log_sizes = [1000, 5000, 10000]

# Define a function to process XES files and gather evaluation metrics
def process_logs(logs_dir, log_size):
    metrics_list = []
    for filename in os.listdir(logs_dir):
        if filename.endswith(f"{log_size}.xes"):
            xes_file_path = os.path.join(logs_dir, filename)
            log = xes_importer.apply(xes_file_path)
            df = xes_converter.apply(log, variant=xes_converter.Variants.TO_DATA_FRAME)
            grouped_by_case_size = df.groupby('case:concept:name').size()
            variant_counts = df.groupby('case:concept:name')['concept:name'].apply(tuple).value_counts()
            metrics = {
                "Log File": filename,
                "Nr Events": len(df),
                "Nr Traces": len(df['case:concept:name'].unique()),
                "Nr Unique Traces": len(df.groupby('case:concept:name')['concept:name'].apply(tuple).unique()),
                "Trace Uniqueness": len(df.groupby('case:concept:name')['concept:name'].apply(tuple).unique()) / len(df['case:concept:name'].unique()),
                "Nr Unique Activities": len(df['concept:name'].unique()),
                "Max Trace Length": grouped_by_case_size.max(),
                "Min Trace Length": grouped_by_case_size.min(),
                "Mean Trace Length": grouped_by_case_size.mean(),
                "Max Nr Traces per Variant": variant_counts.max(),
                "Min Nr Traces per Variant": variant_counts.min(),
                "Mean Nr Traces per Variant": variant_counts.mean(),
                "N-Value for Pripel": grouped_by_case_size.quantile(0.95)
            }
            metrics_list.append(metrics)
    return metrics_list

# Initialize a dictionary to store DataFrames for each log size
dfs_by_log_size = {}

# Process logs for each log size
for log_size in log_sizes:
    simple_metrics = process_logs(simple_logs_dir, log_size)
    complex_metrics = process_logs(complex_logs_dir, log_size)
    all_metrics = simple_metrics + complex_metrics
    df = pd.DataFrame(all_metrics)

    df['Log File'] = df['Log File'].str.replace('_' + str(log_size) + '.xes', '')
    df['Log Complexity'] = df['Log File'].apply(lambda x: 'simple' if '1' in x else 'complex')
    df['Log File'] = df['Log File'].str.replace('1', '')
    df['Log File'] = df['Log File'].str.replace('2', '')
    df.set_index(['Log Complexity', 'Log File'], inplace=True)
    df.sort_index(inplace=True)  # Sorting rows per Log Complexity on Log File
    df = df.reindex(['simple', 'complex'], level='Log Complexity')  # Reindexing to have 'complex' then 'simple' as index in Log Complexity
    print(df)
    dfs_by_log_size[log_size] = df


# Print DataFrames for each log size
for log_size, df in dfs_by_log_size.items():
    print(f"\nMetrics for Log Size: {log_size}")
    print(df)

# Process logs for each log size
for log_size in log_sizes:
    simple_metrics = process_logs(simple_logs_dir, log_size)
    complex_metrics = process_logs(complex_logs_dir, log_size)
    all_metrics = simple_metrics + complex_metrics
    df = pd.DataFrame(all_metrics)

    df['Log File'] = df['Log File'].str.replace('_' + str(log_size) + '.xes', '')
    df['Log Complexity'] = df['Log File'].apply(lambda x: 'simple' if '1' in x else 'complex')
    df['Log File'] = df['Log File'].str.replace('1', '')
    df['Log File'] = df['Log File'].str.replace('2', '')
    df.set_index(['Log Complexity', 'Log File'], inplace=True)
    df.sort_index(inplace=True)  # Sorting rows per Log Complexity on Log File
    df = df.reindex(['simple', 'complex'],
                    level='Log Complexity')  # Reindexing to have 'complex' then 'simple' as index in Log Complexity

    # Export DataFrame to LaTeX
    with open(f"metrics_log_size_{log_size}.tex", "w") as f:
        f.write(df.to_latex())

    dfs_by_log_size[log_size] = df