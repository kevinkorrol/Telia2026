from http import HTTPStatus


def test_projects_seeded(client):
    response = client.get("/api/projects")
    assert response.status_code == HTTPStatus.OK

    projects = response.get_json()
    assert isinstance(projects, list)
    assert projects, "Seeded projects should not be empty"
    assert any(p["name"] == "Customer Portal Redesign" for p in projects)


def test_create_employee_success(client):
    projects_resp = client.get("/api/projects")
    project_id = projects_resp.get_json()[0]["id"]

    payload = {
        "fullName": "Test User",
        "email": "test.user@example.com",
        "experienceLevel": "senior",
        "techStack": "backend",
        "duration": "long",
        "selectedProjects": [project_id],
        "confirmAvailability": True,
    }

    response = client.post("/api/employees", json=payload)
    assert response.status_code == HTTPStatus.CREATED

    data = response.get_json()
    employee = data["employee"]
    assert data["message"] == "Created"
    assert employee["fullName"] == payload["fullName"]
    assert employee["email"] == payload["email"]
    assert employee["selectedProjects"] == [project_id]

    employees_resp = client.get("/api/employees")
    employees = employees_resp.get_json()
    assert any(emp["email"] == payload["email"] for emp in employees)


def test_create_employee_validation_errors(client):
    response = client.post("/api/employees", json={})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    errors = response.get_json().get("details", {})
    assert errors["fullName"] == "fullName is required"
    assert errors["email"] == "email is required"
    assert errors["experienceLevel"] == "experienceLevel is required"
    assert errors["techStack"] == "techStack is required"
    assert errors["duration"] == "duration is required"
    assert errors["selectedProjects"] == "At least one project must be selected"
