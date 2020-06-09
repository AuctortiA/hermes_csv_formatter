import csv
import os
import json
import tkinter as Tk
from tkinter import filedialog
from tkinter import *
import time
from datetime import date

class ProgramRestart(Exception):
    pass


class csv_file:
    def __init__(self, path):
        self.keys = self.load_keys()
        self.settings = self.load_settings()
        self.path = path
        self.content = self.read_file()

    def load_keys(self):
        with open('keys.json', 'r') as keys_file:
            keys = json.load(keys_file)
        return keys

    def load_settings(self):
        with open('settings.json', 'r') as settings_file:
            settings = json.load(settings_file)
        return settings

    def read_file(self):
        print("Reading file...")

        with open(path, newline='') as file:
            dict_reader = csv.DictReader(file, delimiter=self.settings["delimiter"], quotechar=self.settings["quote_char"])
            self.field_names = dict_reader.fieldnames.copy()
            return [ord_dict for ord_dict in dict_reader]

    def remove_blanks(self):
        print("Removing blank lines...")

        self.content = [row for row in self.content if row[self.settings['add1_col']] != ""]

    def convert_del_ref(self):
        print("Converting delivery references...")

        ref_col_name = self.settings['ref_col']
        con_col_name = self.settings['con_col']

        for dict_num, ord_dict in enumerate(self.content):
            for k, v in self.keys.items():
                self.content[dict_num][con_col_name] = self.content[dict_num][con_col_name].replace(k,v)

            self.content[dict_num][ref_col_name] = self.content[dict_num][con_col_name]

    def write_file(self):
        print("Writing to file...")

        with open(f'hermes_output_{date.today()}.csv', 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, delimiter=self.settings["delimiter"], quotechar=self.settings["quote_char"], fieldnames=self.field_names)

            writer.writeheader()
            writer.writerows(self.content)


def get_path():

    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    root.filename = filedialog.askopenfilename(initialdir="/", title="Gimme that csv pls.",
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
            print(f"{'-'*20}| Will's amazing csv thing |{'-'*20}")
            print("\n"*2)

            path = get_path()

            file = csv_file(path)
            time.sleep(1.5)
            file.remove_blanks()
            time.sleep(1.5)
            file.convert_del_ref()
            time.sleep(1.5)
            file.write_file()
            time.sleep(1.5)
            print("ALL DONE!")
            input("Press enter to continue...")
        except ProgramRestart:
           input("Fix error and restart or press enter to continue...")