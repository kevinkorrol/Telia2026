from app import app
from db import db, Project, Employee

def seed_database():
    with app.app_context():
        print("Cleaning up database...")
        db.session.query(Project).delete()
        db.session.query(Employee).delete()
        db.session.commit()  
        
        db.session.expunge_all()

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
        
        employees_data = [
            Employee(full_name="John Doe", email="john.doe@example.com", experience_level="senior", tech_stack="backend", preferred_duration="long", availability_confirmed=True),
            Employee(full_name="Jane Smith", email="jane.smith@example.com", experience_level="mid", tech_stack="frontend", preferred_duration="medium", availability_confirmed=True),
            Employee(full_name="Peter Jones", email="peter.jones@example.com", experience_level="junior", tech_stack="fullstack", preferred_duration="short", availability_confirmed=False),
        ]

        print("Adding new data...")
        db.session.add_all(projects_data)
        db.session.add_all(employees_data)
        
        try:
            db.session.commit()
            print(f"Successfully seeded: {len(projects_data)} projects and {len(employees_data)} employees!")
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {e}")

if __name__ == '__main__':
    seed_database()