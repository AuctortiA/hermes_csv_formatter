import csv
import os
import json


class csv_file:
    def __init__(self, path):
        self.path = path
        self.content = self.read_file()

    def read_file(self):
        print("Reading file...")
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            return [cell for cell in [line for line in reader]]

    def convert_del_ref(self):
        print("Converting delivery references...")
        with open('keys.json') as keys_file:
            keys = json.loads(keys_file)

        reference_row = self.content[0].index('ref')
        for row_num, row in enumerate(self.content):
            ref_cell = row[reference_row]
            if ref_cell in keys.keys():
                self.content[row_num][reference_row] = keys[ref_cell]

    def remove_blanks(self):
        print("Removing blank lines...")
        self.content = [row for row in self.content if row[0] != ""]

    def write_file(self):
        print("Writing to file...")

        with open(f'output.csv', 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(self.content)


if __name__ == '__main__':
    while True:
        print(f"{'-'*20}| Will's amazing csv thing |{'-'*20}")
        print("\n"*2)

        path = input("Please enter .csv path :)\n> ")
        file = csv_file(path)
        file.convert_del_ref()
        file.remove_blanks()
        file.write_file()
        print("ALL DONE!")
        input("Press enter to continue...")
        os.system('cls')
