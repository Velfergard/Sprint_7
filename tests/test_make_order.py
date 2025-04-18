import pytest
import allure
from src import helpers
from src.scooter_api import ScooterApi


class TestMakingOrder:

    @allure.title('Проверка создания заказа с разными значениями поля "color"')
    @allure.description('В тесте создается заказ по сгенерированным корректным данным.'
                        'Через параметры теста передается значение цвета в поле "color".'
                        'После выполнения проверок заказ отменяется.')
    @pytest.mark.parametrize('color', [["BLACK"], ["GRAY"], ["BLACK", "GREY"], []])
    def test_making_order_with_different_colours(self, color, scooter_api):
        data = helpers.generate_order_data_without_color()
        body = {
            "firstName": data["firstName"],
            "lastName": data["lastName"],
            "address": data["address"],
            "metroStation": data["metroStation"],
            "phone": data["phone"],
            "rentTime": data["rentTime"],
            "deliveryDate": data["deliveryDate"],
            "comment": data["comment"],
            "color": color
        }

        response = scooter_api.make_order(body)

        assert response.status_code == 201, f"Некорректный статус-код: {responce.status_code}"
        assert response.json()["track"] is not None

        try:
            data_for_cancel = {"track": response.json()["track"]}
            r = scooter_api.cancel_order(data_for_cancel)
            assert r.status_code == 200

        except:
            pass


    @allure.title('Проверка создания заказа без поля "color"')
    @allure.description('В тесте создается заказ по сгенерированным корректным данным.'
                        'Поле "color" не указывается.'
                        'После выполнения проверок заказ отменяется.')
    def test_making_order_without_color(self, scooter_api):
        data = helpers.generate_order_data_without_color()
        body = {
            "firstName": data["firstName"],
            "lastName": data["lastName"],
            "address": data["address"],
            "metroStation": data["metroStation"],
            "phone": data["phone"],
            "rentTime": data["rentTime"],
            "deliveryDate": data["deliveryDate"],
            "comment": data["comment"]
        }

        response = scooter_api.make_order(body)

        assert response.status_code == 201, f"Некорректный статус-код: {responce.status_code}"
        assert response.json()["track"] is not None

        try:
            data_for_cancel = {"track": response.json()["track"]}
            r = scooter_api.cancel_order(data_for_cancel)
            assert r.status_code == 200

        except:
            pass
