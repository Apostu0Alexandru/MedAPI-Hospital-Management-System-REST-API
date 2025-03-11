# Hospital Management System API

A REST API for managing hospital activities involving Doctors, Patients, Assistants, and Treatments with role-based access control.

## Features

- Role-based access control with three user types: General Manager, Doctor, and Assistant
- Token-based authentication for secure API access
- Complete CRUD operations for all hospital resources
- Treatment recommendation and application tracking
- Patient assignment management
- Detailed reporting capabilities for patient treatments and doctor assignments
- API documentation using OpenAPI/Swagger

## Setup Instructions

### Requirements
- Python 3.9+
- pip

### Installation Steps
1. Clone this repository
   ```
   git clone 
   cd hospital_management
   ```

2. Create and activate a virtual environment (optional)
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Run migrations
   ```
   python manage.py migrate
   ```

5. Create test users (optional)
   ```
   python manage.py create_test_users
   ```

6. Start the server
   ```
   python manage.py runserver
   ```

7. Access the API at http://127.0.0.1:8000/

### Docker Setup (Alternative)
1. Build and start container
   ```
   docker-compose build
   docker-compose up
   ```

2. Access the API at http://localhost:8000/

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `/swagger/`
- ReDoc: `/redoc/`

## API Endpoints

### Authentication
- POST `/api/login/` - Login and obtain token

### Doctors (General Manager only)
- GET, POST `/api/doctors/` - List or create doctors
- GET, PUT, DELETE `/api/doctors/{id}/` - Retrieve, update or delete doctor

### Patients (Doctor or GM)
- GET, POST `/api/patients/` - List or create patients
- GET, PUT, DELETE `/api/patients/{id}/` - Retrieve, update or delete patient

### Assistants (GM only)
- GET, POST `/api/assistants/` - List or create assistants
- GET, PUT, DELETE `/api/assistants/{id}/` - Retrieve, update or delete assistant

### Treatments (Doctor or GM)
- GET, POST `/api/treatments/` - List or create treatments
- GET, PUT, DELETE `/api/treatments/{id}/` - Retrieve, update or delete treatment

### Treatment Recommendations (Doctor)
- GET, POST `/api/treatment-recommendations/` - List or create recommendations

### Treatment Applications (Assistant)
- GET, POST `/api/treatment-applications/` - List or apply treatments

### Patient Assignment (Doctor or GM)
- POST `/api/patient-assignment/` - Assign patient to assistant
- DELETE `/api/patient-assignment/` - Remove patient from assistant

### Reports
- GET `/api/reports/doctors-patients/` - Doctors and patients report (GM)
- GET `/api/reports/patient-treatments/{id}/` - Patient treatments report (GM/Doctor)

## Authentication

The API uses token-based authentication. To authenticate:

1. Obtain a token by sending a POST request to `/api/login/` with your credentials:
   ```
   {
       "username": "manager",
       "password": "manager123"
   }
   ```

2. Include the token in the `Authorization` header of your requests:
   ```
   Authorization: Token 
   ```

## User Roles

1. **General Manager (GM)**: Has access to all endpoints and operations.
2. **Doctor (DR)**: Has access to their patients and can recommend treatments.
3. **Assistant (AS)**: Has access to assigned patients and can apply treatments.

## Live Demo

The API is deployed at [https://medapi-hospital-management-system-rest.onrender.com](https://medapi-hospital-management-system-rest.onrender.com)