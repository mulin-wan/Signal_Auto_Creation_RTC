import os
from tkinter import messagebox
import re

def init_signal_dict():
    # Define a dictionary to map signal attributes to their keys
    signal_attributes = {
        'Signal Number': r'---\s*(\d+)',
        'Begin': r'Begin: (.*?)\s+Via 1:',
        'Via 1': r'Via 1: (.*?)\s+Via 2:',
        'Via 2': r'Via 2: (.*?)\s+End:',
        'End': r'End: (.*?)\s+Speed release:',
        'Speed release': r'Speed release: (.*?)\s*$',
        'Type of signal': r'Type of signal: (.*?)\s{3}',
        'Enabled': r'Enabled: (.*?)\s{3}',
        'Direction': r'Direction: (.*?)\s{3}',
        'Diverging': r'Diverging: (.*?)\s{3}',
        'Check favorable aspects for divergence': r'Check favorable aspects for divergence: (.*?)\s{3}',
        'Continuously lit': r'Continuously lit: (.*?)\s{3}',
        'Virtual': r'Virtual: (.*?)\s{3}',
        'Mast orientation': r'Mast orientation: (.*?)\s{3}',
        'Suppress warnings': r'Suppress warnings: (.*?)\s{3}',
        'Position relative to node': r'Position relative to node: (.*?)\s{3}',
        'Allow guessing': r'Allow guessing: (.*?)\s{3}',
        'Most favorable aspect': r'Most favorable aspect: (.*?)\s{3}',
        'SORS exception distance': r'SORS exception distance: (.*?)\s{5}',
        'Least favorable aspect': r'Least favorable aspect: (.*?)\s{3}',
        'Latency time (MM:SS)': r'Latency time \(MM:SS\): (\s*\d*:?\d*)',
        'Interlocking wait aspect': r'Interlocking wait aspect: (.*?)\s{3}',
        'Number of heads': r'Number of heads: (.*?)\s{3}',
        'Number of affected blocks': r'Number of affected blocks: (.*?)\s{3}',
        'Direction change': r'Direction change: (.*?)\s{3}',
        'Trailing signal direction(s)': r'Trailing signal direction\(s\): (.*?)\s{3}',
    }
    return signal_attributes


def read_signal_file(file_path, signal_attributes):
    with open(file_path, 'r') as file:
        signals = []
        signal = {}
        for line in file:
            line = line.strip()
            if re.match(r'---\s*\d+', line):  # Start of a new signal
                if signal:
                    signals.append(signal)
                signal = {}
            else:
                # Check each attribute in the dictionary
                for attribute, pattern in signal_attributes.items():
                    match = re.search(pattern, line)
                    if match:
                        signal[attribute] = match.group(1)
                # Check if the line is for affected blocks
                affected_block_pattern = r'^(\d+)\s+Begin: (.*?)\s{3}Via 1: (.*?)\s{3}Via 2: (.*?)\s{3}End: (.*?)\s{3}Parent aspect: (.*?)\s{3}Trailing aspect: (.*?)\s{3}$'
                match = re.search(affected_block_pattern, line)
                if match:
                    if 'Affected Blocks' not in signal:
                        signal['Affected Blocks'] = []
                    signal['Affected Blocks'].append({
                        'Block Number': match.group(1),
                        'Begin': match.group(2),
                        'Via 1': match.group(3),
                        'Via 2': match.group(4),
                        'End': match.group(5),
                        'Parent aspect': match.group(6),
                        'Trailing aspect': match.group(7)
                    })
        # Append the last signal
        if signal:
            signals.append(signal)
    print(signal)
    return signals

def print_signal(signals, signal_number):
    for signal in signals:
        if 'Signal Number' in signal and signal['Signal Number'] == str(signal_number):
            print(signal)


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
    
    #print_signal(signals, 210)
    messagebox.showinfo("Success", "Signal processing completed successfully")
