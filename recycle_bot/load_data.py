import json

from recycle_bot import settings
from recycle_bot.gs_api import SpreadsheetAPI

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def load_gs_data(spreadsheet_id, range):
    api = SpreadsheetAPI(settings.API_KEY)
    data = api.spreadsheet_values(spreadsheet_id, range)
    return data


def save_data(data, file_path):
    with open(file_path, 'w') as fh:
        json.dump(data, fh)


def load_data(file_path):
    return json.load(open(file_path))


class DatumManager:
    _keys = None
    _container = None

    def __init__(self, data):
        self.parse_data(data)

    def parse_data(self, data):
        for container, description, keys_str in data:
            self._container[container] = description

            keys = keys_str.split('\n')
            for key in keys:
                if key in self.keys:
                    raise ValueError(f'Wrong data given, duplicate "{key}"')

                self.keys[key] = container

    @property
    def keys(self):
        return self._keys

    @property
    def description(self):
        return self._container

    def get_sub_keys(self, substr):
        result = []
        if len(substr) >= settings.I_Q_MIN_LEN:
            for key in self.keys:
                if len(result) >= settings.I_Q_WORDS_COUNT:
                    break

                if key.startswith(substr):
                    result.append(key)
        return result

    def get_info(self, key):
        if key not in self.keys:
            return None

        return self.description[self.keys[key]]


if __name__ == '__main__':
    save_data(
        load_gs_data(
            settings.SPREADSHEET_ID,
            settings.RANGE_NAME
        ),
        settings.DATA_FILE_PATH
    )
