import pytest
import allure
from src import data
from src import helpers
from src.scooter_api import ScooterApi


class TestCourierLogin:

    @allure.title('Проверка авторизации курьера')
    @allure.description('В тесте создается курьер по сгенерированным корректным данным.'
                        'Дальше происходит попытка логина с этими данными.'
                        'После выполнения проверок курьер удаляется.')
    def test_login_courier_is_possible(self, scooter_api):
        courier = helpers.register_new_courier_and_return_login_password()
        data = {
            "login": courier[0],
            "password": courier[1]
        }
        responce = scooter_api.login_courier(data)

        assert responce.status_code == 200, f"Некорректный статус-код: {responce.status_code}"
        assert responce.json()["id"] is not None

        try:
            r = scooter_api.delete_courier(responce.json()["id"])
            assert r.status_code == 200

        except:
            pass


    @allure.title('Проверка авторизации курьера с пустым логином')
    @allure.description('В тесте создается курьер по сгенерированным корректным данным.'
                        'Дальше происходит попытка логина с пустым логином и корректным паролем.'
                        'После выполнения проверок курьер удаляется.')
    @pytest.mark.parametrize('login', ["", None])
    def test_login_courier_with_null_login(self, scooter_api, login):
        courier = helpers.register_new_courier_and_return_login_password()
        data = {
            "login": login,
            "password": courier[1]
        }
        responce = scooter_api.login_courier(data)

        assert responce.status_code == 400, f"Некорректный статус-код: {responce.status_code}"
        assert "Недостаточно данных" in responce.json()["message"]

        try:
            data_for_del = {
                "login": courier[0],
                "password": courier[1]
            }

            cour_id = helpers.get_courier_id(data_for_del)
            r = scooter_api.delete_courier(cour_id)
            assert r.status_code == 200

        except:
            pass


    # Тест падает из-за бага сервиса, т.к. возвращается 504 статус-код
    @allure.title('Проверка авторизации курьера без поля с паролем')
    @allure.description('В тесте создается курьер по сгенерированным корректным данным.'
                        'Дальше происходит попытка логина без указания пароля.'
                        'После выполнения проверок курьер удаляется.')
    def test_login_courier_without_password(self, scooter_api):
        courier = helpers.register_new_courier_and_return_login_password()
        data = {
            "login": courier[0]
        }
        responce = scooter_api.login_courier(data)

        assert responce.status_code == 400, f"Некорректный статус-код: {responce.status_code}"
        assert "Недостаточно данных" in responce.json()["message"]

        try:
            data_for_del = {
                "login": courier[0],
                "password": courier[1]
            }

            cour_id = helpers.get_courier_id(data_for_del)
            r = scooter_api.delete_courier(cour_id)
            assert r.status_code == 200

        except:
            pass


    @allure.title('Проверка авторизации курьера с несуществующими данными')
    @allure.description('В тесте создается курьер по сгенерированным корректным данным.'
                        'Дальше происходит попытка логина с измененными данными.'
                        'После выполнения проверок курьер удаляется.')
    @pytest.mark.parametrize('login,password', [['', '123'], ['Test', '']])
    def test_login_courier_with_incorrect_data(self, login, password, scooter_api):
        courier = helpers.register_new_courier_and_return_login_password()
        data = {
            "login": courier[0] + login,
            "password": courier[1] + password
        }
        responce = scooter_api.login_courier(data)

        assert responce.status_code == 404, f"Некорректный статус-код: {responce.status_code}"
        assert responce.json()["message"] == "Учетная запись не найдена"

        try:
            data_for_del = {
                "login": courier[0],
                "password": courier[1]
            }

            cour_id = helpers.get_courier_id(data_for_del)
            r = scooter_api.delete_courier(cour_id)
            assert r.status_code == 200

        except:
            pass
