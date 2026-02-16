import requests
import os
from dotenv import load_dotenv
from core.setting.enviroments import Enviroments
from core.clients.endpoints import Endpoints
from core.setting.config import Users, Timeouts
import allure

load_dotenv()


class ApiClients:
    def __init__(self):
        enviroments_str = os.getenv("ENVIROMENTS")
        try:
            enviroments = Enviroments(enviroments_str)
        except KeyError:
            raise ValueError(f"Unsupported ENVIROMENTS value: {enviroments_str}")

        self.base_url = self.get_base_url(enviroments)
        self.session = requests.Session()
        self.session.headers = {
            "Content-Type": "application/json",
        }

    def get_base_url(self, enviroments: Enviroments) -> str:
        if enviroments == Enviroments.TEST:
            return os.getenv("TEST_BASE_URL")
        elif enviroments == Enviroments.PROD:
            return os.getenv("PROD_BASE_URL")
        else:
            raise ValueError(f"Unsupported ENVIROMENTS value: {enviroments}")

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.headers, json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def ping(self):
        with allure.step("Ping api client"):
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step("Assert status code"):
            assert response.status_code == 201, f"Expected status 201 but got {response.status_code}"
        return response.status_code

    def auth(self):
        with allure.step("Getting authenticate"):
            url = f"{self.base_url}{Endpoints.AUTH_ENDPOINT}"
            payload = {"username": Users.USERNAME, "password": Users.PASSWORD}
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()
        with allure.step("Cheching status code"):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        token = response.json()["token"]
        with allure.step("Updating header with authorization"):
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get_booking_by_id(self,booking_id:int,accept:str = "application/json",expected_status:int=200):
        with allure.step(f"Getting booking by ID {booking_id}"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"

            headers = {"Accept": accept}
            response = self.session.get(url, headers=headers)

        with allure.step(f"Assert status code {expected_status}"):
            assert response.status_code == expected_status, f"Expected status {expected_status} but got {response.status_code}Response:{response.text}"
        if accept == "application/json" and response.status_code == 200:
            booking_data = response.json()

            allure.attach(
                str(booking_data),
                name=f"Booking {booking_id} Data",
                attachment_type=allure.attachment_type.JSON
            )
            return booking_data
        elif accept == "application/json" and response.status_code == 200:
            allure.attach(
                response.text,
                name=f"Booking {booking_id} XML Data",
                attachment_type=allure.attachment_type.XML
            )
            return response.text
        else:
            return response.text