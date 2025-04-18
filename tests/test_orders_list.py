import pytest
import allure
from src import data
from src import helpers
from src.scooter_api import ScooterApi


class TestOrdersList:

    @allure.title('Проверка получения списка заказов')
    @allure.description('В тесте получаем список заказ без query-параметров.')
    def test_get_orders_list(self, scooter_api):
        responce = scooter_api.get_orders_list()

        assert responce.status_code == 200, f"Некорректный статус-код: {responce.status_code}"
        assert len(responce.json()["orders"]) > 0


    @allure.title('Проверка получения списка заказов по id курьера')
    @allure.description('В тесте получаем список заказ по query-параметру courierId.')
    def test_get_orders_list_by_courier_id(self, scooter_api):
        cour_id = data.courier_id
        responce = scooter_api.get_orders_list_with_courier_id_param(cour_id)

        assert responce.status_code == 200, f"Некорректный статус-код: {responce.status_code}"
        assert "orders" in responce.json()


    @allure.title('Проверка получения списка заказов по несуществующему id курьера')
    @allure.description('В тесте получаем список заказ по query-параметру courierId, значения которого нет в базе.')
    def test_get_orders_list_by_courier_id_doesnt_exist(self, scooter_api):
        id = 123
        responce = scooter_api.get_orders_list_with_courier_id_param(id)

        assert responce.status_code == 404, f"Некорректный статус-код: {responce.status_code}"
        assert responce.json()["message"] == f"Курьер с идентификатором {id} не найден"


    @allure.title('Проверка получения списка заказов по параметру nearestStation')
    @allure.description('В тесте получаем список заказ по query-параметру nearestStation.'
                        'Проверяем передачу как одного значения, так и нескольких.')
    @pytest.mark.parametrize('station', [["1"], ["20", "100"]])
    def test_get_orders_list_by_near_stations(self, station, scooter_api):
        responce = scooter_api.get_orders_list_with_nearest_station_param(station)

        assert responce.status_code == 200, f"Некорректный статус-код: {responce.status_code}"
        assert len(responce.json()["orders"]) > 0
        assert f'"metroStation": {station[0]}' or f'"metroStation": {station[1]}' in responce.json()["availableStations"]


    @allure.title('Проверка получения списка заказов по параметру limit')
    @allure.description('В тесте получаем список заказ по query-параметру limit.'
                        'Проверяем умолчательные значения, заданное значение и граничные значения.')
    @pytest.mark.parametrize('limit', ['', 'null', 0, 15, 30])
    def test_get_orders_list_by_limit(self, limit, scooter_api):
        responce = scooter_api.get_orders_list_with_limit_param(limit)

        assert responce.status_code == 200, f"Некорректный статус-код: {responce.status_code}"
        if limit == '' or limit == 'null' or limit == 30 or limit == 0:
            assert responce.json()["pageInfo"]["limit"] == 30
        else:
            assert responce.json()["pageInfo"]["limit"] == limit


    @allure.title('Проверка получения списка заказов по параметру page')
    @allure.description('В тесте получаем список заказ по query-параметру page.'
                        'Проверяем умолчательные значения и заданные значения.')
    @pytest.mark.parametrize('page', ['', 'null', 0, 1, 10, 100])
    def test_get_orders_list_by_page(self, page, scooter_api):
        responce = scooter_api.get_orders_list_with_page_number_param(page)

        assert responce.status_code == 200, f"Некорректный статус-код: {responce.status_code}"
        if page == '' or page == 'null' or page == 0:
            assert responce.json()["pageInfo"]["page"] == 0
        else:
            assert responce.json()["pageInfo"]["page"] == page
