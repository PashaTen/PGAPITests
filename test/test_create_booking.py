import allure
import pytest


@allure.feature('CreateBooking')
@allure.story('Successful creation')
def test_create_booking_success(api_client, generate_random_booking_data):
    data = api_client.create_booking(generate_random_booking_data)
    assert isinstance(data["bookingid"], int)
    assert data["booking"]["firstname"] == generate_random_booking_data["firstname"]
    assert data["booking"]["lastname"] == generate_random_booking_data["lastname"]
    assert data["booking"]["bookingdates"] == generate_random_booking_data["bookingdates"]


@allure.feature('CreateBooking')
@allure.story('Booking id is positive number')
def test_create_booking_id_is_positive(api_client, generate_random_booking_data):
    data = api_client.create_booking(generate_random_booking_data)
    assert data["bookingid"] > 0


@allure.feature('CreateBooking')
@allure.story('Deposit paid is returned correctly')
def test_create_booking_deposit_paid(api_client, generate_random_booking_data):
    data = api_client.create_booking(generate_random_booking_data)
    assert data["booking"]["depositpaid"] == generate_random_booking_data["depositpaid"]


@allure.feature('CreateBooking')
@allure.story('Total price is returned correctly')
def test_create_booking_totalprice(api_client, generate_random_booking_data):
    data = api_client.create_booking(generate_random_booking_data)
    assert data["booking"]["totalprice"] == generate_random_booking_data["totalprice"]


@allure.feature('CreateBooking')
@allure.story('Additional needs are returned correctly')
def test_create_booking_additionalneeds(api_client, generate_random_booking_data):
    data = api_client.create_booking(generate_random_booking_data)
    assert data["booking"]["additionalneeds"] == generate_random_booking_data["additionalneeds"]