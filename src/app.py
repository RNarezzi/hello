import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define Claim Model
class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    policy_holder_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    claim_type = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    date_filed = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'policy_holder_name': self.policy_holder_name,
            'email': self.email,
            'claim_type': self.claim_type,
            'description': self.description,
            'amount': self.amount,
            'status': self.status,
            'date_filed': self.date_filed.isoformat() if self.date_filed else None
        }

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        # Load the default configuration
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/insurance_db')
    else:
        # Load the test configuration passed in
        app.config.update(test_config)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # CRUD Endpoints

    @app.route('/claims', methods=['POST'])
    def create_claim():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        required_fields = ['policy_holder_name', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        new_claim = Claim(
            policy_holder_name=data['policy_holder_name'],
            amount=data['amount'],
            email=data.get('email'),
            claim_type=data.get('claim_type'),
            description=data.get('description'),
            status=data.get('status', 'Pending')
        )

        db.session.add(new_claim)
        db.session.commit()

        return jsonify(new_claim.to_dict()), 201

    @app.route('/claims', methods=['GET'])
    def get_claims():
        claims = Claim.query.all()
        return jsonify([claim.to_dict() for claim in claims]), 200

    @app.route('/claims/<int:id>', methods=['GET'])
    def get_claim(id):
        claim = Claim.query.get_or_404(id)
        return jsonify(claim.to_dict()), 200

    @app.route('/claims/<int:id>', methods=['PUT'])
    def update_claim(id):
        claim = Claim.query.get_or_404(id)
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No input data provided'}), 400

        if 'policy_holder_name' in data:
            claim.policy_holder_name = data['policy_holder_name']
        if 'amount' in data:
            claim.amount = data['amount']
        if 'status' in data:
            claim.status = data['status']
        if 'email' in data:
            claim.email = data['email']
        if 'claim_type' in data:
            claim.claim_type = data['claim_type']
        if 'description' in data:
            claim.description = data['description']

        db.session.commit()
        return jsonify(claim.to_dict()), 200

    @app.route('/claims/<int:id>', methods=['DELETE'])
    def delete_claim(id):
        claim = Claim.query.get_or_404(id)
        db.session.delete(claim)
        db.session.commit()
        return jsonify({'message': 'Claim deleted successfully'}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
