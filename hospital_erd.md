```mermaid
erDiagram
    User ||--o{ Doctor : has
    User ||--o{ Assistant : has
    Doctor ||--o{ TreatmentRecommendation : creates
    Doctor }|--|| Patient : treats
    Assistant }|--|| Patient : assists
    Patient ||--o{ TreatmentRecommendation : receives
    Patient ||--o{ TreatmentApplication : receives
    Assistant ||--o{ TreatmentApplication : applies
    Treatment ||--o{ TreatmentRecommendation : recommended_in
    Treatment ||--o{ TreatmentApplication : applied_in

    User {
        int id PK
        string username
        string first_name
        string last_name
        string email
        string role
        string password
    }

    Doctor {
        int id PK
        int user_id FK
        string specialization
        string department
    }

    Assistant {
        int id PK
        int user_id FK
        string department
    }

    Patient {
        int id PK
        string first_name
        string last_name
        date date_of_birth
        text address
        string phone_number
        text medical_history
    }

    Treatment {
        int id PK
        string name
        text description
        decimal cost
    }

    TreatmentRecommendation {
        int id PK
        int doctor_id FK
        int patient_id FK
        int treatment_id FK
        date recommendation_date
        text notes
    }

    TreatmentApplication {
        int id PK
        int assistant_id FK
        int patient_id FK
        int treatment_id FK
        date application_date
        string status
        text notes
    }
```

# Hospital Management System - Entity Relationship Diagram

This diagram represents the relationships between different entities in the Hospital Management System. Here's a breakdown of the relationships:

1. **User Management**
   - Users can be either Doctors or Assistants (one-to-one relationship)
   - Each user has basic information like username, name, email, and role

2. **Doctor-Patient Relationship**
   - Doctors can treat multiple patients (many-to-many relationship)
   - Each patient can be treated by multiple doctors

3. **Assistant-Patient Relationship**
   - Assistants can assist multiple patients (many-to-many relationship)
   - Each patient can have multiple assistants

4. **Treatment Management**
   - Doctors can create treatment recommendations for patients
   - Assistants can apply treatments to patients
   - Each treatment can be recommended or applied multiple times

5. **Treatment Status Tracking**
   - Treatment applications have a status (Pending, In Progress, Completed)
   - Both recommendations and applications include notes for additional information

The system follows a role-based access control system where:
- General Managers (GM) have full access to all entities
- Doctors (DR) can manage their patients and create treatment recommendations
- Assistants (AS) can manage assigned patients and apply treatments 