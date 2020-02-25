import gspread
from oauth2client.service_account import ServiceAccountCredentials


def getCandidatesData():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('Tophire-bba47bacd825.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Sample Candidate List").sheet1
    return sheet.get_all_records()


if __name__ == '__main__':
    print(getCandidatesData())