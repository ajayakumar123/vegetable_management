import pytest
from app import app, db, Vegetable
from flask import url_for
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_vegetable(client):
    response = client.post('/add', data={
        'name': 'Tomato',
        'quantity': 10,
        'expiration_date': '2024-12-31',
        'supplier': 'Local Farm'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Vegetable added successfully!' in response.data

def test_edit_vegetable(client):
    # Add a vegetable first
    vegetable = Vegetable(name='Carrot', quantity=5, expiration_date=datetime.strptime('2024-12-31', '%Y-%m-%d').date(), supplier='Organic Farms')
    db.session.add(vegetable)
    db.session.commit()

    # Edit the vegetable
    response = client.post(f'/edit/{vegetable.id}', data={
        'name': 'Carrot',
        'quantity': 10,
        'expiration_date': '2024-12-31',
        'supplier': 'Organic Farms'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Vegetable updated successfully!' in response.data

def test_delete_vegetable(client):
    # Add a vegetable first
    vegetable = Vegetable(name='Lettuce', quantity=5, expiration_date=datetime.strptime('2024-12-31', '%Y-%m-%d').date(), supplier='Green Farms')
    db.session.add(vegetable)
    db.session.commit()

    # Delete the vegetable
    response = client.post(f'/delete/{vegetable.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'Vegetable deleted successfully!' in response.data
