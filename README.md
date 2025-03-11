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
   git clone https://github.com/Apostu0Alexandru/MedAPI-Hospital-Management-System-REST-API
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

## Testing the API

### 1. Using curl

First, obtain an authentication token:

```bash
# Login to get token
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"manager", "password":"manager123"}'
```

Then use the token to access other endpoints:

#### Doctor Endpoints
```bash
# List all doctors
curl -X GET http://localhost:8000/api/doctors/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"

# Create a new doctor
curl -X POST http://localhost:8000/api/doctors/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{"username":"doctor1", "password":"doctor123", "first_name":"John", "last_name":"Smith", "role":"DR"}'
```

#### Patient Endpoints
```bash
# List all patients
curl -X GET http://localhost:8000/api/patients/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"

# Create a new patient
curl -X POST http://localhost:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{"first_name":"Jane", "last_name":"Doe", "age":"29", "address":"123 Main St", "mobile":"5551234567"}'
```

#### Assistant Endpoints
```bash
# List all assistants
curl -X GET http://localhost:8000/api/assistants/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

#### Treatment Endpoints
```bash
# List all treatments
curl -X GET http://localhost:8000/api/treatments/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

#### Patient Assignments
```bash
# Assign patient to assistant
curl -X POST http://localhost:8000/api/patient-assignments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -d '{"patient":1, "assistant":1}'
```

#### Reports
```bash
# Get doctor-patient report
curl -X GET http://localhost:8000/api/reports/doctors-patients/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### 2. Using Postman

1. Download and install [Postman](https://www.postman.com/downloads/)
2. Create a new request:
   - Set the HTTP method (GET, POST, PUT, DELETE)
   - Enter the URL (e.g., http://localhost:8000/api/doctors/)
   - Add header: `Authorization: Token YOUR_TOKEN_HERE`
   - For POST/PUT requests, add JSON body in the "Body" tab

### 3. Using Swagger UI

1. Start the server: `python manage.py runserver`
2. Navigate to http://localhost:8000/swagger/
3. Authenticate by clicking "Authorize" and entering your token
4. Use the interactive documentation to test all endpoints

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
- POST `/api/patient-assignments/` - Assign patient to assistant
- DELETE `/api/patient-assignments/` - Remove patient from assistant

### Reports
- GET `/api/reports/doctors-patients/` - Doctors and patients report (GM)
- GET `/api/reports/patient-treatments/{id}/` - Patient treatments report (GM/Doctor)

## Live Demo

The API is deployed at [https://medapi-hospital-management-system-rest.onrender.com](https://medapi-hospital-management-system-rest.onrender.com)

