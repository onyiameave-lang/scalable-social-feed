# scalable-social-feed


A backend-focused social feed system built with Flask, PostgreSQL, Redis (planned), and Docker.
This project is designed to simulate real-world scalable social media architecture.


---

Overview

Scalable Social Feed is a backend system that models:

User registration

Posts creation

Follow relationships (many-to-many)

Feed generation logic

Database migrations

Seed data simulation

Containerized PostgreSQL setup


The goal of this project is to practice production-level backend architecture, not just CRUD.


---

Tech Stack

Python 3

Flask

SQLAlchemy (ORM)

PostgreSQL

Docker & Docker Compose

Faker (for test data generation)

Git (version control)



---

Project Structure

scalable-social-feed/
│
├── app.py
├── models.py
├── config.py
├── seed.py
├── migrations/
├── docker-compose.yml
└── README.md


---

Running PostgreSQL with Docker

This project uses Docker to run PostgreSQL.

Start the database

docker compose up -d

This will:

Pull PostgreSQL

Create the database container

Expose port 5432

Persist data using Docker volumes



---

Database Configuration

Example connection string:

postgresql://myuser:mypassword@localhost:5432/scalable_social_feed

If running Flask inside Docker, use:

postgresql://myuser:mypassword@db:5432/scalable_social_feed


---

Migrations

Initialize database:

flask db init

Create migration:

flask db migrate -m "Initial migration"

Apply migration:

flask db upgrade




Seeding Fake Data

Generate fake users, posts, and follow relationships:

python seed.py

This will:

Create random users

Create posts per user

Create random follow relationships

Simulate a real social network graph



Architecture Concepts Practiced

This project focuses on learning:

Many-to-many relationships

Database transactions

Horizontal scaling concepts

Docker container networking

Service separation

Proper commit handling

Data seeding strategies


Future Improvements

Planned upgrades:

Redis caching layer

Feed ranking algorithm

Background workers (Celery)

WebSocket real-time updates

Rate limiting

Structured logging

Performance monitoring

Feed fan-out strategies


🎯 Learning Goal

This project is not just a Flask app.
It is a foundation for understanding how real social platforms scale.

👨‍💻 Author

Emmanuel
Backend Developer
Focused on scalable systems architecture