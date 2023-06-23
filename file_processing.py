import os
from tkinter import messagebox
import re

def init_signal_dict():
    # Define a dictionary to map signal attributes to their keys
    signal_attributes = {
        'Signal Number': r'(\d+)',
        'Begin': r'Begin: (.*?) ',
        'Via 1': r'Via 1: (.*?) ',
        'Via 2': r'Via 2: (.*?) ',
        'End': r'End: (.*?) ',
        'Speed release': r'Speed release: (.*?) ',
        'Type of signal': r'Type of signal: (\w+)',
        'Enabled': r'Enabled:(\w+)',
        'Direction': r'Direction: (\w+)',
        'Diverging': r'Diverging: (\w+)',
        'Check favorable aspects for divergence': r'Check favorable aspects for divergence: (\w+)',
        'Continuously lit': r'Continuously lit: (\w+)',
        'Mast orientation': r'Mast orientation: (\w+)',
        'Position relative to node': r'Position relative to node: (\w+)',
        'Most favorable aspect': r'Most favorable aspect: (\w+)',
        'Least favorable aspect': r'Least favorable aspect: (\w+)',
        'Interlocking wait aspect': r'Interlocking wait aspect: (\w+)',
        'Number of affected blocks': r'Number of affected blocks: (\w+)',
        'Direction change': r'Direction change: (\w+)',
        'Trailing signal direction(s)': r'Trailing signal direction\(s\): (\w+)',
    }
    return signal_attributes

def read_signal_file(file_path, signal_attributes):
    with open(file_path, 'r') as file:
        signals = []
        signal = {}
        for line in file:
            line = line.strip()
            if line.startswith('---'):  # Start of a new signal
                if signal:
                    signals.append(signal)
                signal = {}
            else:
                # Check each attribute in the dictionary
                for attribute, pattern in signal_attributes.items():
                    match = re.search(pattern, line)
                    if match:
                        signal[attribute] = match.group(1)
        # Append the last signal
        if signal:
            signals.append(signal)
    print(signal)
    return signals


def process_files(directory, experiment, block_length, milepost_start, milepost_end):
    folder_path = str(directory)
    experiment_name = str(experiment)
    nominal_signal_block_length = int(block_length)
    milepost_A = float(milepost_start) if milepost_start else None
    milepost_B = float(milepost_end) if milepost_end else None
    milepost_ranges = [(milepost_A, milepost_B)] if milepost_A and milepost_B else None

    signal_file = os.path.join(folder_path, experiment_name + '.signal')
    node_file = os.path.join(folder_path, experiment_name + '.node')
    link_file = os.path.join(folder_path, experiment_name + '.link')
    
    signal_attributes = init_signal_dict()

    if os.path.exists(signal_file):
        signals = read_signal_file(signal_file, signal_attributes)
        # TODO: modify signals based on milepost_ranges and other criteria
    else:
        signals = []
    # TODO: write signals back to the signal file

    # TODO: read and process node and link files, similar to how we processed the signal file
    #print(signals)
    
    messagebox.showinfo("Success", "Signal processing completed successfully")
