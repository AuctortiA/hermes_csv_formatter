import csv
import os
import json
import tkinter
from tkinter import filedialog
import time
from datetime import date
import sys


class ProgramRestart(Exception):
    pass


class CsvFile:
    def __init__(self, path):
        self.keys = load_keys()
        self.settings = load_settings()
        self.path = path
        self.field_names = []
        self.content = self.read_file()

    def read_file(self):
        print("Reading file...")

        with open(path, newline='') as file:
            dict_reader = csv.DictReader(file, delimiter=self.settings["delimiter"], quotechar=self.settings["quote_char"])
            self.field_names = dict_reader.fieldnames.copy()
            return [ord_dict for ord_dict in dict_reader]

    def remove_blanks(self):
        print("Removing blank lines...")
        len_before = len(self.content)
        self.content = [ord_dict for ord_dict in self.content if not all([ord_dict[field_name] == "" for field_name in self.field_names])]
        print(f'Removed {len_before - len(self.content)} blank lines')

    def convert_del_ref(self):
        print("Converting delivery references...")

        ref_col_name = self.settings['ref_col']
        con_col_name = self.settings['con_col']
        end_loop = False
        for dict_num, ord_dict in enumerate(self.content):
            pointer = dict_num + 1

            if pointer == len(self.content):
                for k, v in self.keys.items():
                    self.content[dict_num][con_col_name] = self.content[dict_num][con_col_name].replace(k, v)
                self.content[dict_num][ref_col_name] = self.content[dict_num][con_col_name]
                break

            while all(self.content[pointer][col] == "" for col in ['Address_line_1', 'Address_line_2', 'Address_line_3']) and self.content[dict_num][con_col_name] != "":
                self.content[pointer][con_col_name] = ""
                self.content[dict_num][con_col_name] = "various"
                print(dict_num)
                if pointer == len(self.content)-1:
                    end_loop = True
                    break
                pointer += 1
            else:
                for k, v in self.keys.items():
                    self.content[dict_num][con_col_name] = self.content[dict_num][con_col_name].replace(k,v)
            self.content[dict_num][ref_col_name] = self.content[dict_num][con_col_name]
            if end_loop:
                break

    def fix_addresses(self):
        if self.settings['fix_addr'] == 'True':
            print("Fixing Addresses...")
            for dict_num, ord_dict in enumerate(self.content):
                addr1_col = self.settings['addr1_col']
                addr2_col = self.settings['addr2_col']
                addr3_col = self.settings['addr3_col']

                split_addr = ord_dict[addr1_col].split(',')
                if len(split_addr) == 2:
                    self.content[dict_num][addr1_col] = split_addr[0]
                    self.content[dict_num][addr2_col] = split_addr[1]
                if len(split_addr) == 3:
                    self.content[dict_num][addr1_col] = split_addr[0]
                    self.content[dict_num][addr2_col] = split_addr[1]
                    self.content[dict_num][addr3_col] = split_addr[2]
                if len(split_addr) == 4:
                    self.content[dict_num][addr1_col] = f'{split_addr[0]}, {split_addr[1]}'
                    self.content[dict_num][addr2_col] = split_addr[2]
                    self.content[dict_num][addr3_col] = split_addr[3]

        else:
            print("Fixing Addresses... (skipping...)")

    def capitalise_names(self):
        print("Capitalising names...")
        for dict_num, ord_dict in enumerate(self.content):
            for col in ['Address_line_1', 'Address_line_2', 'Address_line_3', 'Last_name']:
                self.content[dict_num][col] = ord_dict[col].title()
            self.content[dict_num]['Postcode'] = self.content[dict_num]['Postcode'].upper()

    def write_file(self):
        print("Writing to file...")
        file_name = f'hermes_output_{date.today()}.csv'

        root = tkinter.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        path = filedialog.asksaveasfilename(title="Save as", defaultextension=".csv",
                                            initialfile=file_name)

        with open(path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, delimiter=self.settings["delimiter"],
                                    quotechar=self.settings["quote_char"], fieldnames=self.field_names)

            writer.writeheader()
            writer.writerows(self.content)

        print('File saved')


def load_keys():
    with open('keys.json', 'r') as keys_file:
        keys = json.load(keys_file)
    return keys


def load_settings():
    with open('settings.json', 'r') as settings_file:
        settings = json.load(settings_file)
    return settings


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
            sys.stdout.write("\x1b];Heremes Formatter\x07")
            path = get_path()

            file = CsvFile(path)
            time.sleep(1)

            file.remove_blanks()
            time.sleep(1)

            file.convert_del_ref()
            time.sleep(2.5)

            file.remove_blanks()
            time.sleep(1)

            file.fix_addresses()
            time.sleep(1)

            file.capitalise_names()
            time.sleep(0.5)

            file.write_file()

            input("Press enter to convert another file...")
        except ProgramRestart:
            input("\nFix error and restart or press enter to continue...")
        # except Exception as e:
        #     print(e)
        #     input("\nFix error and restart or press enter to continue...")
