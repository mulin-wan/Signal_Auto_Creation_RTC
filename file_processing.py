import os
from tkinter import messagebox
import numpy as np
import re

def read_signal_file(file_path):
    with open(file_path, 'r') as file:
        signals = []
        signal = []
        # Skip the first two lines
        next(file)
        next(file)
        for line in file:
            if line.startswith('---') and signal:  # Start of a new signal
                signals.append(signal)  # If there's an existing signal, append it to the list
                signal = []  # Initialize a new signal
            else:
                signal.append(line)  # Add the line to the signal content
        # Append the last signal
        if signal:
            signals.append(signal)
    return signals

# Float the input parameters
def floating_input(block_length, milepost_begin, milepost_end):
    block_length = float(block_length)
    milepost_begin = float(milepost_begin)
    milepost_end = float(milepost_end)
    return block_length, milepost_begin, milepost_end

# Filter the signal between the inputed milepost range
def filter_signals(signals, block_length, milepost_begin, milepost_end):
    filtered_signals = []
    # Convert the inputs to float
    block_length, milepost_begin, milepost_end = floating_input(block_length, milepost_begin, milepost_end)
    # Check if block_length is zero
    if block_length == 0:
        print("Error: Block length cannot be zero.")
        return
    milepost_blocks = np.arange(milepost_begin, milepost_end + 1, block_length)
    for signal in signals:
        signal_number, begin_milepost, end_milepost = None, None, None
        first_line = signal[1]
        #print("The first line of each signal is:", first_line)
        parts = first_line.split()
        #print("Splited first line is the parts:", parts)
        signal_number = parts[0]
        begin_milepost = float(parts[2].split('_')[1])
        end_milepost = float(parts[8].split('_')[1])
        # Check if the signal spans any of the specified blocks
        if any(block <= begin_milepost < block + block_length or block <= end_milepost < block + block_length for block in milepost_blocks):
            #filtered_signals.append((signal_number, signal))
            filtered_signals.append(signal)
    return filtered_signals

def process_files(directory, experiment, block_length, milepost_begin, milepost_end):
    block_length, milepost_begin, milepost_end = floating_input(block_length, milepost_begin, milepost_end)
    folder_path = str(directory)
    experiment_name = str(experiment)
    nominal_signal_block_length = float(block_length)
    milepost_A = float(milepost_begin) if milepost_begin else None
    milepost_B = float(milepost_end) if milepost_end else None
    milepost_ranges = [(milepost_A, milepost_B)] if milepost_A and milepost_B else None

    signal_file = os.path.join(folder_path, experiment_name + '.signal')
    node_file = os.path.join(folder_path, experiment_name + '.node')
    link_file = os.path.join(folder_path, experiment_name + '.link')
    
    if os.path.exists(signal_file):
        signals = read_signal_file(signal_file)
        filtered_signals = filter_signals(signals, block_length, milepost_begin, milepost_end)
        #print(filtered_signals)
        #verify_filtered_signals(filtered_signals, block_length, milepost_begin, milepost_end)
        # Example usage:
        save_filtered_signals(filtered_signals, 'filtered_signals.signal')
        # TODO: modify signals based on milepost_ranges and other criteria
    else:
        signals = []
    # TODO: write signals back to the signal file

    # TODO: read and process node and link files, similar to how we processed the signal file
    
    #print_signal(signals, 210)
    messagebox.showinfo("Success", "Signal processing completed successfully")

def save_filtered_signals(filtered_signals, file_path):
    with open(file_path, 'w') as file:
        file.write(' ------------------------------------- R T C   76V    S I G N A L    F I L E ----------------------------------------------------------------------------------------------------------------------\n\n')
        for i, signal in enumerate(filtered_signals):
            for line in signal:
                file.write(''.join(line))  # Join the elements of line into a single string and write it to the file
            if i < len(filtered_signals) - 1:  # If this is not the last signal
                file.write(' --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')  # Add separator between signals
