import csv
import os
import json


class csv_file:
    def __init__(self, path):
        self.path = path
        self.content = self.read_file()
        self.keys = self.load_keys()
        self.settings = self.load_settings()

    def load_keys(self):
        with open('keys.json', 'r') as keys_file:
            keys = json.load(keys_file)
        keys = dict((k.lower(), v.lower()) for k, v in keys.items())
        return keys

    def load_settings(self):
        with open('settings.json', 'r') as settings_file:
            settings = json.load(settings_file)
        settings = dict((k.lower(), v.lower()) for k, v in settings.items())
        return settings

    def read_file(self):
        print("Reading file...")

        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.settings["delimiter"], quotechar=self.settings["quotechar"])
            return [cell for cell in [line for line in reader]]

    def convert_del_ref(self):
        print("Converting delivery references...")

        reference_row = self.content[0].index(self.settings['ref_row'])
        for row_num, row in enumerate(self.content):
            ref_cell = row[reference_row]
            if ref_cell.lower() in self.keys.keys():
                self.content[row_num][reference_row] = self.keys[ref_cell.lower()]

    def remove_blanks(self):
        print("Removing blank lines...")
        self.content = [row for row in self.content if row[0] != ""]

    def write_file(self):
        print("Writing to file...")

        with open(f'output.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=self.settings["delimiter"], quotechar=self.settings["quotechar"])
            print(self.content)
            writer.writerows(self.content)


if __name__ == '__main__':
    while True:
        try:
            os.system('cls')
            print(f"{'-'*20}| Will's amazing csv thing |{'-'*20}")
            print("\n"*2)

            path = input("Please enter .csv path :)\n> ")
            file = csv_file(path)
            file.convert_del_ref()
            file.remove_blanks()
            file.write_file()
            print("ALL DONE!")
            input("Press enter to continue...")
        except Exception as e:
            print("error: e")
