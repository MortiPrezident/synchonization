from config import period, path_log, path_name, headers, name_cloud
from synchronization import Synchronization
from time import sleep
from utils import get_info_local
from loguru import logger

if __name__ == "__main__":
    logger.add(path_log)
    logger.info(f"Программа синхронизации начинает работать с директорией {path_name}")
    try:
        logger.info("Создание объекта для синхронизации")
        syn = Synchronization(
            name_cloud=name_cloud, path_name=path_name, headers=headers
        )
        logger.info("объект создан")
    except Exception as e:
        logger.error(f"Произошла ошибка при создании объекта для синхронизации -  {e}")

    while True:

        sleep(int(period))
        local_data = get_info_local(path_name)
        syn.synchronization(local_data)
