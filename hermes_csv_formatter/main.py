import csv
import os
import json
import tkinter
import sys

from tkinter import filedialog

from .csv_file import CSVFile
from .exceptions import ProgramRestart


def get_path():

    root = tkinter.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    root.filename = filedialog.askopenfilename(initialdir="/", title="Choose a csv file",
                                               filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

    path = root.filename

    if not os.path.isfile(path):
        print("Invalid path make sure you got the right one!")
        raise ProgramRestart
    return path


if __name__ == '__main__':
    while True:
        try:
            os.system('cls')
            sys.stdout.write("\x1b];Hermes Formatter\x07")
            path = get_path()

            file = CSVFile(path)

            file.remove_blanks()

            file.convert_del_ref()

            file.remove_blanks()

            file.fix_addresses()

            file.capitalise_names()

            file.write_file()

            input("Press enter to convert another file...")
        except ProgramRestart:
            input("\nFix error and restart or press enter to try again...")
        # except Exception as e:
        #     print(e)
        #     input("\nFix error and restart or press enter to continue...")
