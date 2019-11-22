import os
from runpy import run_path

local_settings = os.environ.copy()

local_settings_file = local_settings.get('LOCAL_SETTINGS_FILE') or '.local_settings.py'

if os.path.exists(local_settings_file):
    local_settings = run_path(local_settings_file)

DATA_FILE_PATH = local_settings.get('DATA_FILE_PATH') or 'results.json'

# telegram bot params
TOKEN = local_settings.get('TOKEN')
PROXY = local_settings.get('PROXY')
ADMIN_UID = int(local_settings.get('ADMIN_UID', 0))
# inline query params
I_Q_MIN_LEN = local_settings.get('I_Q_MIN_LEN') or 3
I_Q_WORDS_COUNT = local_settings.get('I_Q_WORDS_COUNT') or 5

# google sheet params
API_KEY = local_settings.get('API_KEY')
SPREADSHEET_ID = local_settings.get('SPREADSHEET_ID')
RANGE_NAME = local_settings.get('RANGE_NAME', 'A2:C8')
