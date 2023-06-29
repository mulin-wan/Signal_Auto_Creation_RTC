from tkinter import Tk
from gui import setup_gui

def main():
    root = Tk()
    root.geometry('350x180')
    root.title('Signal Creation Automation')  # setting the title
    setup_gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
