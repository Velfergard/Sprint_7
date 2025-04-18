import requests
import allure
import json
from src import helpers


class ScooterApi:

    def __init__(self, url):
        self.url = url

    @allure.step('Отправить запрос создания курьера')
    def create_courier(self, payload):
        response = requests.post(f"{self.url}/courier", json=payload)

        return response

    @allure.step('Отправить запрос логина курьера')
    def login_courier(self, payload):
        response = requests.post(f"{self.url}/courier/login", json=payload)

        return response

    @allure.step('Отправить запрос удаления курьера')
    def delete_courier(self, id):
        responce = requests.delete(f"{self.url}/courier/{id}")

        return responce

    @allure.step('Отправить запрос создания заказа')
    def make_order(self, payload):
        response = requests.post(f"{self.url}/orders", json=payload)

        return response

    @allure.step('Отправить запрос отмены заказа')
    def cancel_order(self, payload):
        responce = requests.put(f"{self.url}/orders/cancel", json=payload)

        return responce

    @allure.step('Отправить запрос на получение списка заказов')
    def get_orders_list(self):
        response = requests.get(f"{self.url}/orders")

        return response

    @allure.step('Отправить запрос на получение списка заказов по id курьера')
    def get_orders_list_with_courier_id_param(self, id):
        response = requests.get(f"{self.url}/orders?courierId={id}")

        return response

    @allure.step('Отправить запрос на получение списка заказов по ближайшим станциям метро')
    def get_orders_list_with_nearest_station_param(self, station):
        # Сереализация нужна, т.к. бэк принимает только двойные кавычки в query-параметре
        data = json.dumps(station)
        response = requests.get(f"{self.url}/orders?nearestStation={data}")

        return response

    @allure.step('Отправить запрос на получение списка заказов с ограничением по кол-ву заказов на странице')
    def get_orders_list_with_limit_param(self, limit):
        response = requests.get(f"{self.url}/orders?limit={limit}")

        return response

    @allure.step('Отправить запрос на получение списка заказов с конкретной страницы показа заказов')
    def get_orders_list_with_page_number_param(self, page):
        response = requests.get(f"{self.url}/orders?page={page}")

        return response
