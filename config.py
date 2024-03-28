import os
from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

path_name = os.getenv("PATH_NAME")
period = os.getenv("SYNCHRONIZATION_PERIOD")
path_log = os.getenv("PATH_LOG")
name_cloud = os.getenv("NAME_CLOUD")


token = os.getenv("TOKEN")
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"OAuth {token}",
}
