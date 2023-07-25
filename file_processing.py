import os
import re
from tkinter import messagebox

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

def read_node_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        nodes = []
        node = []
        for line in lines[10:]:
            if node:  # If there's an existing node, append it to the list
                nodes.append(node)
                node = []  # Initialize a new node
            else:
                node.append(line)  # Add the line to the node content
        # Append the last node if it hasn't been appended yet
        if node:
            nodes.append(node)
    return nodes

def read_link_file(file_path):
    with open(file_path, 'r') as file:
        links = {}
        lines = file.readlines
        for line in lines[10:]:
            line = line.split()
            if not line:
                continue
            links[line[0]] = line[1:]
    return links

def signal_dict(file_path):
    signals_list = read_signal_file(file_path)
    signals = []

    for signal in signals_list:
        signal_dict = {}
        affected_blocks = []
        num_affected_blocks = None
        for line in signal:
            # Skip the line if it's just hyphens or whitespace
            if line.strip() == '' or line.startswith('-' * 66):
                continue
            # Split the line into segments by multiple spaces
            segments = re.split(r'\s{2,}', line.strip())
            for segment in segments:
                # Partition each segment into key-value pair
                key, _, value = segment.partition(":")
                key = key.strip()
                value = value.strip()

                if key == 'SORS exception distance':
                    # Extract the value from the correct position
                    value = line.split(':')[1].split()[0]
                elif key == 'Number of affected blocks':
                    # Extract the value from the correct position
                    value = line.split(':')[1].split()[0]
                    num_affected_blocks = int(value) if value else 0
                    print(num_affected_blocks)
                if num_affected_blocks is not None and key == 'Begin':
                    # We're in the affected blocks section
                    affected_blocks.append({key: value})
                else:
                    signal_dict[key] = value

            # If we're in the affected blocks section and have read all affected blocks, reset the counter
            if num_affected_blocks is not None and len(affected_blocks) == num_affected_blocks:
                signal_dict['Affected Blocks'] = affected_blocks
                num_affected_blocks = None

        signals.append(signal_dict)

    return signals

def link_dict(filename):
    links = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines[12:]:
            columns = re.split(r'\s\s+', line.strip())
            origin_node, destination_node, bool_list = columns[:3]
            origin_milepost = float(origin_node[2:])  # get milepost from origin node
            destination_milepost = float(destination_node[2:])  # get milepost from destination node
            direction = bool_list[4]
            next_node_1 = columns[5] if '_' in columns[5] else None
            next_node_2 = columns[6] if '_' in columns[6] else None

            links[line] = {
                "origin_node": origin_node,
                "destination_node": destination_node,
                "direction": direction,
                "next_node_1": next_node_1,
                "next_node_2": next_node_2
            }
    return links

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

def switch(signals, links):
    for line in links:
        if links[line]["next_node_2"] is not None:
            for signal in signals:
                if links[line]["origin_node"] not in signal["Begin"]:
# TODO:
                    return 0

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
        nodes = read_node_file(node_file)
        links = link_dict(link_file)
        filtered_signals = filter_signals(signals, block_length, milepost_begin, milepost_end)
        # Example usage:
        save_filtered_signals(filtered_signals, experiment_name + '.SIGNAL')
        signals_dict = signal_dict(signal_file)
        # TODO: modify signals based on milepost_ranges and other criteria
    else:
        signals = []

    # TODO: read and process node and link files, similar to how we processed the signal file

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