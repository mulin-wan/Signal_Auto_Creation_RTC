from tkinter import StringVar, Label, Entry, Button, DoubleVar, filedialog
from file_processing import process_files

def browse_directory(directory):
    directory.set(filedialog.askdirectory())

def setup_gui(root):
    Label(root, text='Directory Path').grid(row=0, column=0)
    directory = StringVar()
    Entry(root, textvariable=directory).grid(row=0, column=1)
    Button(root, text="Browse", command=lambda: browse_directory(directory)).grid(row=0, column=2)

    Label(root, text='Experiment Name').grid(row=1, column=0)
    experiment = StringVar()
    Entry(root, textvariable=experiment).grid(row=1, column=1)

    Label(root, text='Signal Block Length').grid(row=2, column=0)
    block_length = DoubleVar()
    Entry(root, textvariable=block_length).grid(row=2, column=1)

    Label(root, text='Milepost Begin').grid(row=3, column=0)
    milepost_begin = DoubleVar()
    Entry(root, textvariable=milepost_begin).grid(row=3, column=1)

    Label(root, text='Milepost End').grid(row=4, column=0)
    milepost_end = DoubleVar()
    Entry(root, textvariable=milepost_end).grid(row=4, column=1)

    Button(root, text="Process Files", command=lambda: process_files(directory.get(), experiment.get(), block_length.get(), milepost_begin.get(), milepost_end.get())).grid(row=5, column=1)

