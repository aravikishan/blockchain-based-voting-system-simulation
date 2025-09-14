import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_register_voter():
    response = client.post('/register_voter/', json={'voter_id': 'voter1', 'eligible': True})
    assert response.status_code == 200
    assert response.json() == {'voter_id': 'voter1', 'eligible': True}


def test_add_candidate():
    response = client.post('/add_candidate/', json={'candidate_id': 'candidate1', 'name': 'Alice'})
    assert response.status_code == 200
    assert response.json() == {'candidate_id': 'candidate1', 'name': 'Alice', 'vote_count': 0}


def test_cast_vote():
    client.post('/register_voter/', json={'voter_id': 'voter1', 'eligible': True})
    response = client.post('/cast_vote/', json={'transaction_id': 'voter1', 'candidate_id': 'candidate1', 'timestamp': '2023-10-01T12:00:00Z'})
    assert response.status_code == 200
    assert response.json() == {'transaction_id': 'voter1', 'candidate_id': 'candidate1', 'timestamp': '2023-10-01T12:00:00Z'}
