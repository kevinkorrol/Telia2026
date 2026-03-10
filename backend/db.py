from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    experience_level = db.Column(db.String(50))
    tech_stack = db.Column(db.String(100))
    preferred_duration = db.Column(db.String(50))
    additional_skills = db.Column(db.Text)
    availability_confirmed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    projects = db.relationship('Project', secondary='employee_projects', backref='employees')

class EmployeeProject(db.Model):
    __tablename__ = 'employee_projects'
    
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), primary_key=True)