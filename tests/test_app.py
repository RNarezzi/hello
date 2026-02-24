import unittest
import json
from src.app import create_app, db

class TestClaimAPI(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        test_config = {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
        }
        self.app = create_app(test_config)
        self.client = self.app.test_client()

        # Create tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_claim(self):
        response = self.client.post('/claims', json={
            'policy_holder_name': 'John Doe',
            'amount': 5000.0,
            'email': 'john@example.com',
            'claim_type': 'Auto',
            'description': 'Fender bender'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['policy_holder_name'], 'John Doe')
        self.assertEqual(data['status'], 'Pending')
        self.assertIsNotNone(data['id'])

    def test_get_claims(self):
        # Create a claim first
        self.client.post('/claims', json={
            'policy_holder_name': 'Jane Doe',
            'amount': 1200.0
        })

        response = self.client.get('/claims')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]['policy_holder_name'], 'Jane Doe')

    def test_get_single_claim(self):
        # Create a claim
        create_response = self.client.post('/claims', json={
            'policy_holder_name': 'Bob Smith',
            'amount': 300.0
        })
        claim_id = json.loads(create_response.data)['id']

        response = self.client.get(f'/claims/{claim_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['policy_holder_name'], 'Bob Smith')

    def test_update_claim(self):
        # Create a claim
        create_response = self.client.post('/claims', json={
            'policy_holder_name': 'Alice Jones',
            'amount': 100.0
        })
        claim_id = json.loads(create_response.data)['id']

        response = self.client.put(f'/claims/{claim_id}', json={
            'status': 'Approved',
            'amount': 150.0
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'Approved')
        self.assertEqual(data['amount'], 150.0)

    def test_delete_claim(self):
        # Create a claim
        create_response = self.client.post('/claims', json={
            'policy_holder_name': 'Charlie Brown',
            'amount': 50.0
        })
        claim_id = json.loads(create_response.data)['id']

        response = self.client.delete(f'/claims/{claim_id}')
        self.assertEqual(response.status_code, 200)

        # Verify it's gone
        get_response = self.client.get(f'/claims/{claim_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_claim_not_found(self):
        response = self.client.get('/claims/999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
