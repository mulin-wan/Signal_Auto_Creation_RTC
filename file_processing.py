import os
from tkinter import messagebox

def read_signal_file(file_path):
    # Define a dictionary to map signal attributes to their keys
    signal_attributes = {
        'Type of signal': 'Type of signal:',
        'Direction': 'Direction:',
        'Continuously lit': 'Continuously lit:',
        'Mast orientation': 'Mast orientation:',
        'Position relative to node': 'Position relative to node:',
        'Most favorable aspect': 'Most favorable aspect:',
        'Least favorable aspect': 'Least favorable aspect:',
        'Interlocking wait aspect': 'Interlocking wait aspect:',
        'Number of affected blocks': 'Number of affected blocks:',
        'Direction change': 'Direction change:',
        'Trailing signal direction(s)': 'Trailing signal direction(s):',
        'Enabled': 'Enabled:',
        'Diverging': 'Diverging:',
        'Check favorable aspects for divergence': 'Check favorable aspects for divergence:',
        'Virtual': 'Virtual:',
        'Suppress warnings': 'Suppress warnings:',
        'Allow guessing': 'Allow guessing:',
        'SORS exception distance': 'SORS exception distance:',
        'Latency time (MM:SS)': 'Latency time (MM:SS):',
        'Number of heads': 'Number of heads:'
    }

    with open(file_path, 'r') as file:
        signals = []
        signal = {}
        for line in file:
            line = line.strip()
            if "Begin:" in line:
                # Start of a new signal
                if signal:
                    signals.append(signal)
                signal = {
                    'Begin': line.split('Begin:')[1].split('Via 1:')[0].strip(),
                    'Via 1': line.split('Via 1:')[1].split('Via 2:')[0].strip() if 'Via 1:' in line else '',
                    'Via 2': line.split('Via 2:')[1].split('End:')[0].strip() if 'Via 2:' in line else '',
                    'End': line.split('End:')[1].split('Speed release:')[0].strip(),
                }
            else:
                # Check each attribute in the dictionary
                for attribute, key in signal_attributes.items():
                    if line.startswith(key):
                        signal[attribute] = line.split(key)[1].strip()
                        break
        # Append the last signal
        if signal:
            signals.append(signal)
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

    if os.path.exists(signal_file):
        signals = read_signal_file(signal_file)
        # TODO: modify signals based on milepost_ranges and other criteria
    else:
        signals = []
    # TODO: write signals back to the signal file

    # TODO: read and process node and link files, similar to how we processed the signal file
    #print(signals)
    print(signals)
    messagebox.showinfo("Success", "Signal processing completed successfully")
