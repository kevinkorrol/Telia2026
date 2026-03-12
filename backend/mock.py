from flask import current_app
from db import db, Project, Employee, EmployeeProject

def seed_database(app=None, *, reset: bool = False) -> None:
    app = app or current_app
    with app.app_context():
        if reset:
            db.session.query(EmployeeProject).delete()
            db.session.query(Employee).delete()
            db.session.query(Project).delete()
            db.session.commit()

        projects_missing = db.session.query(Project).count() == 0
        employees_missing = db.session.query(Employee).count() == 0

        if projects_missing:
            projects_data = [
                Project(name="Customer Portal Redesign"),
                Project(name="Data Pipeline Migration"),
                Project(name="Mobile App Enhancement"),
                Project(name="Internal Analytics Dashboard"),
                Project(name="API Gateway Implementation"),
                Project(name="Cloud Infrastructure Setup"),
                Project(name="E-commerce Platform Update"),
                Project(name="Reporting System Automation"),
                Project(name="Microservices Architecture Transition"),
                Project(name="Customer Data Platform Integration"),
            ]
            db.session.add_all(projects_data)

        if employees_missing:
            employees_data = [
                Employee(full_name="John Doe", email="john.doe@example.com", experience_level="senior", tech_stack="backend", preferred_duration="long", availability_confirmed=True),
                Employee(full_name="Jane Smith", email="jane.smith@example.com", experience_level="mid", tech_stack="frontend", preferred_duration="medium", availability_confirmed=True),
                Employee(full_name="Peter Jones", email="peter.jones@example.com", experience_level="junior", tech_stack="fullstack", preferred_duration="short", availability_confirmed=False),
            ]
            db.session.add_all(employees_data)

        if projects_missing or employees_missing:
            db.session.commit()

if __name__ == '__main__':
    from app import app
    seed_database(app, reset=True)