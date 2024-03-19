import requests
from loguru import logger


class Synchronization:

    def __init__(self, name_cloud, path_name, headers):
        self.name_cloud = name_cloud
        self.path_name = path_name
        self.headers = headers

    def load(self, path):
        try:
            logger.info(f'Загрузка файла {path} в облако')
            response = requests.get(
                f'https://cloud-api.yandex.net/v1/disk/resources/upload?path={self.name_cloud}{path}',
                headers=self.headers).json()

            href = response['href']

            with open(self.path_name + path, 'rb') as f:
                r = requests.put(href, data=f)
            logger.info(f'Файл {path} загружен')
        except Exception as e:
            logger.error(f'Ошибка при загрузке файла - {e}')
            logger.error(f'ответ сервера - {r.json()}')

    def reload(self, path):
        try:
            logger.info(f'Перезапись файла {path} в облако')
            response = requests.get(
                f'https://cloud-api.yandex.net/v1/disk/resources/upload?path={self.name_cloud}{path}&overwrite=true',
                headers=self.headers).json()

            href = response['href']

            with open(self.path_name + path, 'rb') as f:
                r = requests.put(href, data=f)
            logger.info(f'Файл {path} перезаписан')
        except Exception as e:
            logger.error(f'Ошибка при перезаписи файла - {e}')
            logger.error(f'ответ сервера - {r.json()}')

    def delete(self, path):
        try:
            logger.info(f'Удаление файла {path} из облака')
            response = requests.delete(
                f'https://cloud-api.yandex.net/v1/disk/resources?path={self.name_cloud}{path}&permanently=true',
                headers=self.headers)
            logger.info(f'файл {path} успешно удалён')

        except Exception as e:
            logger.error(f'Ошибка при удалении файла - {e}')
            logger.error(f'ответ сервера - {response.json()}')

    def synchronization(self, locale):
        try:
            logger.info('Начало синхронизации')
            cloud = self.get_info_cloud()
            locale_keys = locale.keys()
            cloud_keys = cloud.keys()
            for elem in locale_keys:
                if elem not in cloud_keys:
                    self.load(elem)
                    cloud[elem] = locale[elem]

                if locale[elem] != cloud[elem]:
                    self.reload(elem)

            for elem in cloud_keys:
                if elem not in locale_keys:
                    self.delete(elem)
            logger.info('конец  синхронизации')
        except Exception as e:
            logger.error(f'ошибка при синхронизации - {e}')

    def get_info_cloud(self):
        try:
            logger.info('Получение информации о файлах в облаке')
            data = requests.get(
                f'https://cloud-api.yandex.net/v1/disk/resources?path={self.name_cloud}'
                '&fields=_embedded.items.name,_embedded.items.size,_embedded.items.type',
                headers=self.headers).json()
            data_list = data['_embedded']['items']
            data_dict = {}
            for elem in data_list:
                if elem['type'] == 'dir':
                    continue
                name = elem['name']
                size = elem['size']
                data_dict[name] = size
                logger.debug(f"В облаке находится файл '{name}' размером {size} байт")

            logger.info('информация получена')
        except Exception as e:
            logger.error(f'Не получилось получить информацию о файлах - {e}')
            logger.error(f'ответ сервера - {data}')

        return data_dict
