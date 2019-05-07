import pytest
from flask import json

from tests.users.user_factory import UserFactory


@pytest.mark.usefixtures('_db')
class TestAuth:
    def test_no_token_for_missing_person(self, client):
        resp = client.post('/auth/login', json={'id': 'missing'})
        assert resp.status_code == 403

        data = json.loads(resp.data)
        assert data['message'] == 'User not found'

    def test_token_and_user_for_found_user(self, client, UserFactory):
        user = UserFactory()

        resp = client.post('/auth/login', json={'id': user.id})
        assert resp.status_code == 200

        data = json.loads(resp.data)
        assert 'token' in data

        expected_user = {'id': user.id, 'name': user.name, 'email': user.email}
        assert data['user'] == expected_user
