from flask import Flask, jsonify, request
from flask_cors import *
from backend.mock import seed_database
from db import db, Employee, Project
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///telia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)

with app.app_context():
    db.create_all()
    try:
        seed_database(app)
    except Exception as exc:
        app.logger.warning("Seeding skipped: %s", exc)

def post_employee(employee: Employee, data: dict) -> None:
    employee.full_name = data.get('fullName', '').strip()
    employee.email = data.get('email', '').strip().lower()
    employee.experience_level = data.get('experienceLevel', '').strip()
    employee.tech_stack = data.get('techStack', '').strip()
    employee.preferred_duration = data.get('duration', '').strip()
    employee.additional_skills = data.get('additionalSkills', '').strip()
    employee.availability_confirmed = bool(data.get('confirmAvailability', False))

    selected_ids = data.get('selectedProjects', [])
    if not isinstance(selected_ids, list):
        selected_ids = []

    projects = Project.query.filter(Project.id.in_(selected_ids)).all() if selected_ids else []
    employee.projects = projects


def serialize_employee(employee: Employee) -> dict:
    return {
        'id': employee.id,
        'fullName': employee.full_name,
        'email': employee.email,
        'experienceLevel': employee.experience_level,
        'techStack': employee.tech_stack,
        'selectedProjects': [project.id for project in employee.projects],
        'duration': employee.preferred_duration or '',
        'additionalSkills': employee.additional_skills or '',
        'confirmAvailability': bool(employee.availability_confirmed),
    }

# endpoint to fetch all projects for dropdown
@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([{'id': p.id, 'name': p.name} for p in projects])

# endpoint to create/update employee
@app.route('/api/employees', methods=['POST'])
def save_employee():
    data = request.get_json(silent=True) or {}

    # Validation
    required_fields = ["fullName", "email", "experienceLevel", "techStack", "duration"]
    errors = {}

    # Check required fields
    for field in required_fields:
        if not str(data.get(field, '')).strip():
            errors[field] = f'{field} is required'

    # Validate email format
    email = str(data.get('email', '')).strip().lower()
    if email and not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        errors['email'] = 'Invalid email format'

    # Validate at least one project
    selected_ids = data.get('selectedProjects', [])
    if not isinstance(selected_ids, list) or len(selected_ids) == 0:
        errors['selectedProjects'] = 'At least one project must be selected'

    # Return errors if any
    if errors:
        return jsonify({'error': 'Validation failed', 'details': errors}), 400

    employee = Employee.query.filter_by(email=email).first()
    created = employee is None

    if created:
        employee = Employee()
        db.session.add(employee)

    post_employee(employee, data)
    db.session.commit()

    return jsonify({
        'message': 'Created' if created else 'Updated',
        'employee': serialize_employee(employee)
    }), 201 if created else 200

# simple endpoint to fetch all employees for testing purposes
@app.route('/api/employees', methods=['GET'])
def get_all_employees():
    employees = Employee.query.all()
    return jsonify([serialize_employee(e) for e in employees])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)