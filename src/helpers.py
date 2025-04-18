import requests
import random
import string
from src import data
from datetime import date, timedelta

# метод регистрации нового курьера возвращает список из логина и пароля
# если регистрация не удалась, возвращает пустой список
def register_new_courier_and_return_login_password():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # возвращаем список
    return login_pass


def generate_courier_data():
    def gen_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login = gen_random_string(10)
    password = gen_random_string(10)
    first_name = gen_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    return payload


def get_courier_id(payload):
    body = {
        "login": payload["login"],
        "password": payload["password"]
    }
    responce = requests.post(f"{data.scooter_url}/courier/login", json=body)
    id = responce.json()["id"]

    return id


def gen_phone():
    phone_base = ""
    operator_code = [
        "900", "901", "902", "903", "904", "905", "906", "908", "909", "910", "911", "912", "913", "914", "915", "916",
        "917", "918", "919", "920", "921", "922", "923", "924", "925", "926", "927", "928", "929", "930", "931", "932",
        "933", "934", "936", "937", "938", "939", "941", "942", "949", "950", "951", "952", "953", "954", "955", "956",
        "958", "959", "960", "961", "962", "963", "964", "965", "966", "967", "968", "969", "970", "971", "977", "978",
        "979", "980", "981", "982", "983", "984", "985", "986", "987", "988", "989", "990", "991", "992", "993", "994",
        "995", "996", "997", "999"
        ]
    for num in range(0, 7):
        phone_base += str(random.randint(0, 9))

    phone = random.choice(operator_code) + phone_base

    return phone


def gen_rent_time():
    rent_time = random.randint(1, 7)

    return rent_time


def gen_delivery_date():
    sysdate = date.today()
    delivery_date = (sysdate + timedelta(random.randint(0, 7))).strftime("%Y.%m.%d")

    return delivery_date


def generate_order_data_without_color():
    def gen_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    body = {
        "firstName": gen_random_string(7),
        "lastName": gen_random_string(7),
        "address": f"г. Москва, ул. {gen_random_string(7)}, д. 11",
        "metroStation": gen_random_string(7),
        "phone": gen_phone(),
        "rentTime": gen_rent_time(),
        "deliveryDate": gen_delivery_date(),
        "comment": "Доставить к подъезду №5!"
    }

    return body
