from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from hospital.models import Doctor, Assistant, Patient, Treatment

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates test users with different roles for the hospital system'

    def handle(self, *args, **kwargs):
        # Create General Manager
        if not User.objects.filter(username='manager').exists():
            gm_user = User.objects.create_user(
                username='manager',
                email='manager@hospital.com',
                password='manager123',
                first_name='John',
                last_name='Manager',
                role='GM'
            )
            self.stdout.write(self.style.SUCCESS(f'Created General Manager: {gm_user.username}'))
        
        # Create Doctor
        if not User.objects.filter(username='doctor').exists():
            doctor_user = User.objects.create_user(
                username='doctor',
                email='doctor@hospital.com',
                password='doctor123',
                first_name='Jane',
                last_name='Doctor',
                role='DR'
            )
            doctor = Doctor.objects.create(
                user=doctor_user,
                specialization='Cardiology',
                department='Cardiology'
            )
            self.stdout.write(self.style.SUCCESS(f'Created Doctor: {doctor_user.username}'))
        
        # Create Assistant
        if not User.objects.filter(username='assistant').exists():
            assistant_user = User.objects.create_user(
                username='assistant',
                email='assistant@hospital.com',
                password='assistant123',
                first_name='Mike',
                last_name='Assistant',
                role='AS'
            )
            assistant = Assistant.objects.create(
                user=assistant_user,
                department='Cardiology'
            )
            self.stdout.write(self.style.SUCCESS(f'Created Assistant: {assistant_user.username}'))
            
        # Create some patients
        if Patient.objects.count() == 0:
            doctor = Doctor.objects.first()
            for i in range(1, 4):
                patient = Patient.objects.create(
                    first_name=f'Patient{i}',
                    last_name='Test',
                    date_of_birth='1990-01-01',
                    address=f'Address {i}',
                    phone_number=f'12345{i}',
                    medical_history=f'History for patient {i}'
                )
                patient.doctors.add(doctor)
                self.stdout.write(self.style.SUCCESS(f'Created Patient: {patient.first_name} {patient.last_name}'))
        
        # Create some treatments
        if Treatment.objects.count() == 0:
            treatments = [
                {'name': 'Blood Test', 'description': 'Standard blood work', 'cost': 50.00},
                {'name': 'X-Ray', 'description': 'Chest X-Ray', 'cost': 120.00},
                {'name': 'MRI', 'description': 'Full body scan', 'cost': 500.00}
            ]
            for t in treatments:
                treatment = Treatment.objects.create(**t)
                self.stdout.write(self.style.SUCCESS(f'Created Treatment: {treatment.name}'))
                
        self.stdout.write(self.style.SUCCESS('All test users and data created successfully!'))
        self.stdout.write(self.style.SUCCESS('Login credentials:'))
        self.stdout.write(self.style.SUCCESS('- General Manager: username="manager", password="manager123"'))
        self.stdout.write(self.style.SUCCESS('- Doctor: username="doctor", password="doctor123"'))
        self.stdout.write(self.style.SUCCESS('- Assistant: username="assistant", password="assistant123"'))
