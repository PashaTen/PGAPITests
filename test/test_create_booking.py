import allure
import pytest
import requests
from requests import HTTPError

VALID_PAYLOAD = {
    "firstname": "Jim",
    "lastname": "Brown",
    "totalprice": 111,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2018-01-01",
        "checkout": "2019-01-01"
    },
    "additionalneeds": "Breakfast"
}

@allure.feature('Test CreateBooking')
@allure.story('Test successful booking creation')
def test_create_booking_success(api_client):
    data = api_client.create_booking(VALID_PAYLOAD)
    assert isinstance(data['bookingid'], int)
    assert data['booking']['firstname'] == VALID_PAYLOAD['firstname']
    assert data['booking']['lastname'] == VALID_PAYLOAD['lastname']
    assert data['booking']['bookingdates'] == VALID_PAYLOAD['bookingdates']

@allure.feature('Test CreateBooking')
@allure.story('Missing required field')
@pytest.mark.parametrize("field",['firstname','lastname','totalprice','depositpaid','bookingdates'])
def test_create_booking_missing_field(api_client,mocker, field):
    payload = {k: v for k, v in VALID_PAYLOAD.items() if k != field}
    mock_response = mocker.Mock(status_code=400)
    mock_response.raise_for_status.side_effect = HTTPError ("400 Client Error")
    mocker.patch.object(api_client, 'post',return_value=mock_response)
    with pytest.raises(HTTPError):
        api_client.create_booking(payload)

@allure.feature('Test CreateBooking')
@allure.story('Server unavailable')
def test_create_booking_server_unavailable(api_client,mocker):
    mocker.patch.object(api_client.session,'post',side_effect=HTTPError ("Server unavailable"))
    with pytest.raises(Exception,match="Server unavailable"):
        api_client.create_booking(VALID_PAYLOAD)

@allure.feature('Test CreateBooking')
@allure.story('Timeout')
def test_create_booking_timeout(api_client,mocker):
    mocker.patch.object(api_client.session,'post',side_effect=requests.Timeout)
    with pytest.raises(requests.Timeout):
        api_client.create_booking(VALID_PAYLOAD)
