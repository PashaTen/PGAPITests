import allure
import pytest




@allure.feature('Test ping')
@allure.story('Test connection')
def test_ping(api_client):
    status_code = api_client.ping()
    assert status_code == 201, f"Expected status code 201, got {status_code}"

@allure.feature('Test ping')
@allure.story('Test server unavailable')
def test_ping_server_unavailable(api_client,mocker):
    mocker.patch.object(api_client.session,'get',side_effect=Exception("Server unavailable"))
    with pytest.raises(Exception,match="Server unavailable"):
        api_client.ping()