import pytest
import json
from django.test import TestCase, Client
from tests.factories import UserFactory

class UserShow(TestCase):
    def test_user_show(self):
        user = UserFactory()
        client = Client()
        response = client.get(f"/api/v1/user/{user.id}/")

        assert response.status_code == 200
        content = json.loads(response.content)
        assert isinstance(content, dict)
        assert len(content) == 1
        assert isinstance(content['data'], dict)
        assert len(content['data']) == 3

        entry = content['data']
        assert isinstance(entry['type'], str)
        assert entry['type'] == 'User'
        assert isinstance(entry['id'], str)
        assert isinstance(entry['attributes'], dict)
        assert len(entry['attributes']) == 3
        assert isinstance(entry['attributes']['name'], str)
        assert isinstance(entry['attributes']['lat'], str)
        assert isinstance(entry['attributes']['lon'], str)


    def test_user_show_404(self):
        user = UserFactory()
        client = Client()
        response = client.get(f"/api/v1/user/{user.id + 1}/")
        assert response.status_code == 404

        content = json.loads(response.content)
        assert isinstance(content, dict)
        assert len(content) == 1
        assert isinstance(content['errors'], list)
        assert len(content['errors']) == 1

        error = content['errors'][0]
        assert isinstance(error, dict)
        assert len(error) == 3
        assert error['detail'] == 'Not found.'
        assert error['status'] == '404'
        assert error['code'] == 'not_found'