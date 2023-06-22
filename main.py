from tkinter import Tk
from gui import setup_gui

def main():
    root = Tk()
    root.geometry('350x250')
    setup_gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
