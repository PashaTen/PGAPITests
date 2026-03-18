import allure
import pytest
from requests import HTTPError
from core.models.booking import BookingResponse


@allure.feature('CreateBooking')
@allure.story('Successful creation')
def test_create_booking_success(api_client,generate_random_booking_data):
    response = api_client.create_booking(generate_random_booking_data)
    booking_response = BookingResponse(**response)
    assert booking_response.bookingid > 0
    assert booking_response.booking.firstname == generate_random_booking_data["firstname"]
    assert booking_response.booking.lastname == generate_random_booking_data["lastname"]
    assert booking_response.booking.totalprice == generate_random_booking_data["totalprice"]
    assert booking_response.booking.depositpaid == generate_random_booking_data["depositpaid"]
    assert str(booking_response.booking.bookingdates.checkin) == generate_random_booking_data["bookingdates"]["checkin"]
    assert str(booking_response.booking.bookingdates.checkout) == generate_random_booking_data["bookingdates"][
        "checkout"]
    assert booking_response.booking.additionalneeds == generate_random_booking_data["additionalneeds"]

@allure.feature('CreateBooking')
@allure.story('Successful creation without firstname')
def test_create_booking_without_firstname(api_client, generate_random_booking_data):
    del generate_random_booking_data["firstname"]
    with pytest.raises(HTTPError):
        api_client.create_booking(generate_random_booking_data)

@allure.feature('CreateBooking')
@allure.story('Creation without lastname')
def test_create_booking_without_lastname(api_client, generate_random_booking_data):
    del generate_random_booking_data["lastname"]
    with pytest.raises(HTTPError):
        api_client.create_booking(generate_random_booking_data)