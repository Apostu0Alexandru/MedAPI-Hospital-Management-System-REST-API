from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Doctor, Assistant, Patient, Treatment, TreatmentRecommendation, TreatmentApplication

User = get_user_model()

class HospitalAPITests(APITestCase):
    def setUp(self):
        # Create users for testing
        self.gm_user = User.objects.create_user(
            username='gm_user', password='password123', role='GM'
        )
        self.doctor_user = User.objects.create_user(
            username='doctor_user', password='password123', role='DR'
        )
        self.assistant_user = User.objects.create_user(
            username='assistant_user', password='password123', role='AS'
        )
        
        # Create doctor and assistant profiles
        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            specialization='Cardiology',
            department='Heart'
        )
        
        self.assistant = Assistant.objects.create(
            user=self.assistant_user,
            department='Heart'
        )
        
        # Create a patient
        self.patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth='1990-01-01',
            address='123 Main St',
            phone_number='123-456-7890',
        )
        
        # Associate patient with doctor
        self.patient.doctors.add(self.doctor)
        
        # Create a treatment
        self.treatment = Treatment.objects.create(
            name='Blood Test',
            description='Standard blood work',
            cost=99.99
        )
    
    def test_login(self):
        url = reverse('login')
        data = {'username': 'gm_user', 'password': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['role'], 'GM')
    
    def test_doctor_list_as_gm(self):
        self.client.force_authenticate(user=self.gm_user)
        url = reverse('doctor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_patient_list_as_doctor(self):
        self.client.force_authenticate(user=self.doctor_user)
        url = reverse('patient-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should see their patient
    
    def test_create_treatment_recommendation(self):
        self.client.force_authenticate(user=self.doctor_user)
        url = reverse('treatmentrecommendation-list')
        data = {
            'patient': self.patient.id,
            'treatment': self.treatment.id,
            'notes': 'Recommended blood test'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TreatmentRecommendation.objects.count(), 1)
