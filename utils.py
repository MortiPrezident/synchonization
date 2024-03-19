import os
import requests
from loguru import logger


def get_info_local(path_name) -> dict:

    """
        Функция предназначенная для получения словаря содержащего имя и размер файла

    """

    try:
        logger.info('Получение локальных данных ')
        list_file = os.listdir(path_name)
        file_dict = {}
        for elem in list_file:
            if os.path.isfile(f'{path_name}/{elem}'):
                size_file = os.path.getsize(f'{path_name}/{elem}')
                file_dict[elem] = size_file
                logger.debug(f"В дирректории {path_name} находится файл '{elem}' размером {size_file} байт")
        logger.info('Данные получены')
    except Exception as e:
        logger.error('Ошибка при получении данных - ', e)
    return file_dict


