import pytest
from _pytest import monkeypatch
from flask import json

from tests.users.user_factory import UserFactory

mp = monkeypatch.MonkeyPatch()


@pytest.mark.usefixtures('_db')
class TestGetUser:
    def test_invalid_id_response_code(self, client):
        resp = client.get('/users/123')
        assert resp.status_code == 404

    def test_valid_id_response_code_and_response(self, client, UserFactory):
        user = UserFactory()

        resp = client.get('/users/%s' % user.id)
        assert resp.status_code == 200

        data = json.loads(resp.data)

        expected = {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }

        assert data == expected


@pytest.mark.usefixtures('_db')
class TestUpdateUser:
    def test_update_invalid_id_response_code(self, client):
        # patch current user
        mp.setattr('api.endpoints.users.get_jwt_identity', lambda: '123')

        resp = client.put('/users/123', json={
            'name': 'New Name',
            'email': 'new@example.com'
        })
        assert resp.status_code == 404

    def test_update_valid_id_response_code_and_response(self, client, UserFactory):
        user = UserFactory(id='123', name='Old Name')

        # patch current user
        mp.setattr('api.endpoints.users.get_jwt_identity', lambda: '123')

        resp = client.put('/users/%s' % user.id, json={
            'name': 'New Name',
            'email': 'new@example.com'
        })
        assert resp.status_code == 200

        data = json.loads(resp.data)

        expected = {
            'id': user.id,
            'name': 'New Name',
            'email': user.email
        }

        assert data == expected
