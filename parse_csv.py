import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv


def parseCsv(filePath):
    columnNames = ["First Name", "Last Name ", "Email Address", "Mobile Number", "Resume"]
    op = []
    with open(filePath) as csvFile:
        reader = csv.DictReader(csvFile, delimiter=",")
        count = 0
        for row in reader:
            if count == 0:
                count += 1
                continue
            op.append(row)
    return op


def getCandidatesData():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('Tophire-bba47bacd825.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Sample Candidate List").sheet1
    return sheet.get_all_records()


if __name__ == '__main__':
    print(parseCsv("/Users/saurabhmardikar/Downloads/Sample Candidate List - Sheet1.csv"))
    # print(getCandidatesData())