from flask import Flask, jsonify, request
from flask_cors import *
from db import db, Employee, Project

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///telia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)

@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([{'id': p.id, 'name': p.name} for p in projects])

@app.route('/api/employees', methods=['POST'])
def save_employee():
    data = request.json
    # TODO: Add validation and save logic. If user exists, update instead of create.
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)