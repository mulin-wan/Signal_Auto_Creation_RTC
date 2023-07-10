import os
from tkinter import messagebox
import numpy as np
import re

def read_signal_file(file_path):
    with open(file_path, 'r') as file:
        signals = []
        signal = []
        for line in file:
            if line.strip() == '' or line.startswith('-' * 66):  # Start of a new signal or empty line
                if signal:  # If there's an existing signal, append it to the list
                    signals.append(signal)
                signal = []  # Initialize a new signal
            else:
                signal.append(line)  # Add the line to the signal content
        # Append the last signal if it hasn't been appended yet
        if signal:
            signals.append(signal)
    del signals[0]
    return signals

# Filter the signal between the inputed milepost range
def filter_signals(signals, block_length, milepost_begin, milepost_end):
    filtered_signals = []
    # Check if block_length is zero
    if block_length == 0:
        print("Warning: Block length is zero. The output signal is empty now.")
        return
    for signal in signals:
        signal_number, signal_begin, signal_end = None, None, None
        first_line = signal[1]
        first_attributes = first_line.split()
        signal_number = int(first_attributes[0])
        signal_begin = float(first_attributes[2].split('_')[1])
        signal_end = float(first_attributes[8].split('_')[1])
        signal_interval = signal_end - signal_begin
        # Check if the signal spans any of the specified blocks
        if signal_begin >= milepost_begin:
            if signal_end <= milepost_end:
                if signal_interval > block_length:
                    filtered_signals.append(signal)
    return filtered_signals

def process_files(directory, experiment, block_length, milepost_begin, milepost_end):
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
        # Example usage:
        save_filtered_signals(filtered_signals, experiment_name + '.SIGNAL')
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
        if filtered_signals is None:
            return
        for i, signal in enumerate(filtered_signals):
            for line in signal:
                file.write(''.join(line))  # Join the elements of line into a single string and write it to the file
            if i < len(filtered_signals) - 1:  # If this is not the last signal
                file.write('\n')  # Add separator between signals
