import pytest
import allure
from src import helpers
from src.scooter_api import ScooterApi


class TestCourierCreation:

    @allure.title('Проверка создания курьера')
    @allure.description('В тесте создается курьер по сгенерированным корректным данным.'
                        'После выполнения проверок курьер удаляется.')
    def test_create_courier_is_possible(self, scooter_api):
        data = helpers.generate_courier_data()
        responce = scooter_api.create_courier(data)

        assert responce.status_code == 201, f"Некорректный статус-код: {responce.status_code}"
        assert '{"ok":true}' in responce.text, f"Некорректное тело ответа: {responce.text}"

        try:
            cour_id = helpers.get_courier_id(data)
            r = scooter_api.delete_courier(cour_id)
            assert r.status_code == 200

        except:
            pass


    @allure.title('Проверка создания курьера-дубликата')
    @allure.description('В тесте создается курьер по данным, уже существующим в системе.'
                        'После выполнения проверок курьер удаляется.')
    def test_create_courier_duplicate_error(self, scooter_api):
        courier = helpers.register_new_courier_and_return_login_password()
        data = {
            "login": courier[0],
            "password": courier[1],
            "firstName": courier[2]
        }
        responce = scooter_api.create_courier(data)

        assert responce.status_code == 409, f"Некорректный статус-код: {responce.status_code}"
        assert "логин уже используется" in responce.json()["message"]

        try:
            cour_id = helpers.get_courier_id(data)
            r = scooter_api.delete_courier(cour_id)
            assert r.status_code == 200

        except:
            pass


    @allure.title('Проверка создания курьера с уже существующим логином')
    @allure.description('В тесте создается курьер с логином, который уже существует в системе.'
                        'После выполнения проверок курьер удаляется.')
    def test_create_courier_with_existed_login(self, scooter_api):
        courier = helpers.register_new_courier_and_return_login_password()
        data = {
            "login": courier[0],
            "password": "qwert1234",
            "firstName": "Existed Login"
        }
        responce = scooter_api.create_courier(data)

        assert responce.status_code == 409, f"Некорректный статус-код: {responce.status_code}"
        assert "логин уже используется" in responce.json()["message"]

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


    @allure.title('Проверка создания курьера без обязательных полей')
    @allure.description('В тесте создается курьер по данным, в которых отсутствует значение либо логина, либо пароля.')
    @pytest.mark.parametrize('objects', [["test1", "", "Testov Test"], ["", "qwer123", "Test Testov"]])
    def test_create_courier_without_required_object(self, objects, scooter_api):
        data = {
            "login": objects[0],
            "password": objects[1],
            "firstName": objects[2]
        }
        responce = scooter_api.create_courier(data)

        assert responce.status_code == 400, f"Некорректный статус-код: {responce.status_code}"
        assert "Недостаточно данных для создания учетной записи" == responce.json()["message"]
