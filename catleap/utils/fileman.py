import csv


class ToCsv:
    def __init__(self, csv_path, rowNames):
        self.__CSV_PATH = csv_path
        with open(self.__CSV_PATH, "w") as f:
            writer = csv.writer(f)
            writer.writerow(rowNames)

    def writeRow(self, rowData):
        with open(self.__CSV_PATH, "a") as f:
            writer = csv.writer(f)
            writer.writerow(rowData)
