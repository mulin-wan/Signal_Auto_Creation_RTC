import os
from tkinter import messagebox
import numpy as np
import re

def read_signal_file(file_path):
    with open(file_path, 'r') as file:
        signals = []
        signal = {}
        signal_content = []
        for line in file:
            line = line.strip()
            if line.startswith('---'):  # Start of a new signal
                if signal:  # If there's an existing signal, append it to the list
                    signal['Content'] = '\n'.join(signal_content)
                    signals.append(signal)
                signal = {}  # Initialize a new signal
                signal_content = []  # Reset signal content
                next_line = file.readline().strip()  # Read the next line
                match = re.search(r'(\d+)', next_line)  # Try to extract the signal number
                if match:  # If a match was found
                    signal_number = match.group(1)
                    signal['Signal Number'] = signal_number
                signal_content.append(next_line)  # Add the line to the signal content
            else:
                signal_content.append(line)  # Add the line to the signal content
                if 'Begin:' in line:
                    signal['Begin'] = line.split('Begin:')[1].split()[0]
                if 'End:' in line:
                    signal['End'] = line.split('End:')[1].split()[0]
        # Append the last signal
        if signal:
            signal['Content'] = '\n'.join(signal_content)
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
        # Check if 'Begin' and 'End' keys exist in signal
        if 'Begin' in signal and 'End' in signal:
            # Extract milepost from 'Begin' and 'End' fields
            begin_milepost = float(signal['Begin'].split('_')[1])
            end_milepost = float(signal['End'].split('_')[1])
            # Check if the signal spans any of the specified blocks
            if any(block <= begin_milepost < block + block_length or block <= end_milepost < block + block_length for block in milepost_blocks):
                filtered_signals.append(signal)
    return filtered_signals

def verify_filtered_signals(filtered_signals, block_length, milepost_begin, milepost_end):
    block_length, milepost_begin, milepost_end = floating_input(block_length, milepost_begin, milepost_end)
    milepost_blocks = milepost_blocks = np.arange(milepost_begin, milepost_end + 1, block_length)
    for signal in filtered_signals:
        begin_milepost = float(signal['Begin'].split('_')[1])
        end_milepost = float(signal['End'].split('_')[1])
        if not any(block <= begin_milepost < block + block_length or block <= end_milepost < block + block_length for block in milepost_blocks):
            print(f"Signal Number: {signal['Signal Number']} does not fall within the specified blocks.")
            return False
    print("All signals fall within the specified blocks.")
    return True

def save_filtered_signals(filtered_signals, file_path):
    with open(file_path, 'w') as file:
        file.write(' ------------------------------------- R T C   76V    S I G N A L    F I L E ----------------------------------------------------------------------------------------------------------------------\n\n')
        file.write(' --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
        for signal in filtered_signals:
            file.write(signal['Content'])
            file.write('\n --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')  # Add separator between signals

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
        verify_filtered_signals(filtered_signals, block_length, milepost_begin, milepost_end)
        # Example usage:
        save_filtered_signals(filtered_signals, 'filtered_signals.signal')
        # TODO: modify signals based on milepost_ranges and other criteria
    else:
        signals = []
    # TODO: write signals back to the signal file

    # TODO: read and process node and link files, similar to how we processed the signal file
    
    #print_signal(signals, 210)
    messagebox.showinfo("Success", "Signal processing completed successfully")