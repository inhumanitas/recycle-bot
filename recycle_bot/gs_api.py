from requests_oauthlib import OAuth2Session


class SpreadsheetAPIError(Exception):
    pass


class SpreadsheetAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = OAuth2Session()

    def terminate(self):
        self.session.close()

    def request(self, url):
        with self.session.get(url) as resp:
            if resp.status_code != 200:
                raise SpreadsheetAPIError(resp)
            return resp.json()

    def spreadsheet_info(self, spreadsheet_id: str):
        url = (
            f'https://sheets.googleapis.com/v4/'
            f'spreadsheets/{spreadsheet_id}/?key={self.api_key}')
        body = self.request(url)
        return body

    def spreadsheet_values(self, spreadsheet_id: str, range: str):
        url = (
            f'https://sheets.googleapis.com/v4/'
            f'spreadsheets/{spreadsheet_id}/values/{range}?key={self.api_key}')
        body = self.request(url)
        return body['values']