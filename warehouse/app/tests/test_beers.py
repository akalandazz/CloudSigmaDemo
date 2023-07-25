'''
Test the beers operations


Use the beer_fixture to have data to retrieve, it generates three type of beers
'''
from unittest.mock import ANY
import http.client
from freezegun import freeze_time
from .constants import PRIVATE_KEY
from wh import token_validation
from faker import Faker
fake = Faker()


@freeze_time('2019-05-07 13:47:34')
def test_create_beer(client):
    new_beer = {
        'name': fake.text(30),
    }
    header = token_validation.generate_token_header(fake.name(),
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }
    response = client.post('/api/beers/', data=new_beer,
                           headers=headers)
    result = response.json

    assert http.client.CREATED == response.status_code

    expected = {
        'id': ANY,
        'name': new_beer['name'],
        'timestamp': '2019-05-07T13:47:34',
    }
    assert result == expected


def test_create_beer_unauthorized(client):
    new_beer = {
        'name': fake.text(30),
    }
    response = client.post('/api/beers/', data=new_beer)
    assert http.client.UNAUTHORIZED == response.status_code


def test_list_beers(client, beer_fixture):
    username = fake.name()
    name = fake.text(30)

    # Create a new beer
    new_beer = {
        'name': name,
    }
    header = token_validation.generate_token_header(username,
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }
    response = client.post('/api/beers/', data=new_beer,
                           headers=headers)

    assert http.client.CREATED == response.status_code

    # Get the beers of the user
    response = client.get('/api/beers/', headers=headers)
    results = response.json

    assert http.client.OK == response.status_code
    assert len(results) == 5


def test_list_beers_search(client, beer_fixture):
    username = fake.name()
    new_beer = {
        'name': 'lowenbrau'
    }
    header = token_validation.generate_token_header(username,
                                                    PRIVATE_KEY)
    headers = {
        'Authorization': header,
    }
    response = client.post('/api/beers/', data=new_beer,
                           headers=headers)
    assert http.client.CREATED == response.status_code

    response = client.get('/api/beers/?search=lowenbrau')
    result = response.json

    assert http.client.OK == response.status_code
    assert len(result) > 0

    # Check that the returned values contain "lowenbrau"
    for beer in result:
        expected = {
            'name': ANY,
            'id': ANY,
            'timestamp': ANY,
        }
        assert expected == beer
        assert 'lowenbrau' in beer['name'].lower()


def test_get_beer(client, beer_fixture):
    beer_id = beer_fixture[0]
    response = client.get(f'/api/beers/{beer_id}/')
    result = response.json

    assert http.client.OK == response.status_code
    assert 'name' in result
    assert 'timestamp' in result
    assert 'id' in result


def test_get_non_existing_beer(client, beer_fixture):
    beer_id = 123456
    response = client.get(f'/api/beers/{beer_id}/')

    assert http.client.NOT_FOUND == response.status_code
