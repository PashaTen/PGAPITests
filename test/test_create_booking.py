import allure
import pytest


@allure.feature('CreateBooking')
@allure.story('Successful creation')
def test_create_booking_success(api_client,generate_random_booking_data):
    data = api_client.create_booking(generate_random_booking_data)
    assert isinstance(data["bookingid"], int)
    assert data["bookingid"] > 0
    assert data["booking"]["firstname"] == generate_random_booking_data["firstname"]
    assert data["booking"]["lastname"] == generate_random_booking_data["lastname"]
    assert data["booking"]["totalprice"] == generate_random_booking_data["totalprice"]
    assert data["booking"]["depositpaid"] == generate_random_booking_data["depositpaid"]
    assert data["booking"]["bookingdates"] == generate_random_booking_data["bookingdates"]
    assert data["booking"]["additionalneeds"] == generate_random_booking_data["additionalneeds"]

@allure.feature('CreateBooking')
@allure.story('Successful creation without firstname')
def test_create_booking_without_firstname(api_client,generate_random_booking_data):
    del generate_random_booking_data["firstname"]
    with pytest.raises(Exception):
        api_client.create_booking(generate_random_booking_data)