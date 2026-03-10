from app import app
from db import db, Project

def seed_database():
    with app.app_context():
        if Project.query.first():
            print("Database already has data. Deleting existing projects...")
            Project.query.delete()
            db.session.commit()
        
        projects = [
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
        
        db.session.add_all(projects)
        db.session.commit()
        print("Database seeded with projects!")

if __name__ == '__main__':
    seed_database()