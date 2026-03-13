# Telia2026

## Architecture
- Frontend: Svelte + TypeScript + Vite dev server. Runs on port 5173 inside Docker
- Backend: Flask. Runs on port 5000 inside Docker.
- Data: SQLite database file lives in backend directory; created and seeded on backend startup via mock.seed_database when empty.
- Containers: Docker Compose builds two services (frontend, backend)

## API Endpoints
- GET /api/projects — returns list of projects `[ { id, name } ]`.
- GET /api/employees — returns list of employees with project IDs. Endpoint for testing purposes
- POST /api/employees — body JSON:
	- Required: fullName (string), email (email string), experienceLevel (string), techStack (string), duration (string), selectedProjects (array of project IDs; at least one).
	- Optional: additionalSkills (string), confirmAvailability (bool).
	- Behavior: creates or updates by email. Returns 201 with `{ message, employee }` if created, 200 if updated; 400 with validation details on error.

## Run with Docker
1) From repo root: `docker compose up --build`
2) Frontend at http://localhost:5173, backend API at http://localhost:5000

### Seeding and resetting data
- Initial data seeds on backend start only when the SQLite file is empty.
