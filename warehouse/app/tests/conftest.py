import pytest
import http.client
from wh.app import create_app
from .constants import PRIVATE_KEY
from wh import token_validation
from faker import Faker
fake = Faker()


@pytest.fixture
def app():
    application = create_app()

    application.app_context().push()
    # Initialise the DB
    application.db.create_all()

    return application


@pytest.fixture
def beer_fixture(client):
    '''
    Generate three beers in the system.
    '''

    beer_ids = []
    for _ in range(3):
        beer = {
            'name': fake.text(30),
        }
        header = token_validation.generate_token_header(fake.name(),
                                                        PRIVATE_KEY)
        headers = {
            'Authorization': header,
        }
        response = client.post('/api/beers/', data=beer,
                               headers=headers)
        assert http.client.CREATED == response.status_code
        result = response.json
        beer_ids.append(result['id'])

    yield beer_ids

    # Clean up all beers
    response = client.get('/api/beers/')
    beers = response.json
    for beer in beers:
        beer_id = beer['id']
        url = f'/admin/beers/{beer_id}/'
        response = client.delete(url)
        assert http.client.NO_CONTENT == response.status_code
