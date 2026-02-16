import requests
import os
from dotenv import load_dotenv
from core.setting.enviroments import Enviroments

load_dotenv()


class ApiClients:
    def __init__(self):
        enviroments_str = os.getenv("ENVIROMENTS")
        try:
            enviroments = Enviroments(enviroments_str)
        except KeyError:
            raise ValueError(f"Unsupported ENVIROMENTS value: {enviroments_str}")

        self.base_url = self.get_base_url(enviroments)
        self.headers = {
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
