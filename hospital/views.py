from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token




from .models import Doctor, Assistant, Patient, Treatment, TreatmentRecommendation, TreatmentApplication
from .serializers import (DoctorSerializer, AssistantSerializer, PatientSerializer,
                         TreatmentSerializer, TreatmentRecommendationSerializer,
                         TreatmentApplicationSerializer, UserSerializer)
from .permissions import IsGeneralManager, IsDoctor, IsAssistant, IsDoctorOrGeneralManager

class LoginView(APIView):
    """
    API endpoint for user authentication and token generation.
    """
    permission_classes = []  # No authentication required for login
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'error': 'Please provide both username and password'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        # Get or create token
        token, created = Token.objects.get_or_create(user=user)
        
        # Return token and user role information
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'role': user.role,  # Access the role field you defined
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)

# Doctor views
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsGeneralManager]

# Assistant views
class AssistantViewSet(viewsets.ModelViewSet):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer
    permission_classes = [IsGeneralManager]

# Patient views
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsDoctorOrGeneralManager]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'GM':
            return Patient.objects.all()
        elif user.role == 'DR':
            return Patient.objects.filter(doctors=user.doctor)
        return Patient.objects.none()

# Treatment views
class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer
    permission_classes = [IsDoctorOrGeneralManager]

# Treatment Recommendation views
class TreatmentRecommendationViewSet(viewsets.ModelViewSet):
    queryset = TreatmentRecommendation.objects.all()
    serializer_class = TreatmentRecommendationSerializer
    permission_classes = [IsDoctor]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'GM':
            return TreatmentRecommendation.objects.all()
        elif user.role == 'DR':
            return TreatmentRecommendation.objects.filter(doctor=user.doctor)
        return TreatmentRecommendation.objects.none()
    
    def perform_create(self, serializer):
        doctor = self.request.user.doctor
        serializer.save(doctor=doctor)

# Treatment Application views
class TreatmentApplicationViewSet(viewsets.ModelViewSet):
    queryset = TreatmentApplication.objects.all()
    serializer_class = TreatmentApplicationSerializer
    permission_classes = [IsAssistant]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'AS':
            return TreatmentApplication.objects.filter(assistant=user.assistant)
        return TreatmentApplication.objects.none()
    
    def perform_create(self, serializer):
        assistant = self.request.user.assistant
        serializer.save(assistant=assistant)

# Patient Assignment (assistants to patients)
class PatientAssignmentView(APIView):
    permission_classes = [IsDoctorOrGeneralManager]
    
    def post(self, request):
        patient_id = request.data.get('patient_id')
        assistant_id = request.data.get('assistant_id')
        
        patient = get_object_or_404(Patient, id=patient_id)
        assistant = get_object_or_404(Assistant, id=assistant_id)
        
        patient.assistants.add(assistant)
        return Response({'message': 'Assistant assigned to patient successfully'})
    
    def delete(self, request):
        patient_id = request.data.get('patient_id')
        assistant_id = request.data.get('assistant_id')
        
        patient = get_object_or_404(Patient, id=patient_id)
        assistant = get_object_or_404(Assistant, id=assistant_id)
        
        patient.assistants.remove(assistant)
        return Response({'message': 'Assistant removed from patient successfully'})

# Reports
class DoctorPatientsReportView(APIView):
    permission_classes = [IsGeneralManager]
    
    def get(self, request):
        doctors = Doctor.objects.all()
        result = []
        
        total_patients = Patient.objects.count()
        
        for doctor in doctors:
            patients = doctor.patients.all()
            result.append({
                'doctor': {
                    'id': doctor.id,
                    'name': f"{doctor.user.first_name} {doctor.user.last_name}",
                    'specialization': doctor.specialization
                },
                'patients': PatientSerializer(patients, many=True).data,
                'patient_count': patients.count()
            })
        
        # Statistics
        statistics = {
            'total_doctors': doctors.count(),
            'total_patients': total_patients,
            'average_patients_per_doctor': total_patients / doctors.count() if doctors.count() > 0 else 0
        }
        
        return Response({
            'doctors_data': result,
            'statistics': statistics
        })

class PatientTreatmentsReportView(APIView):
    permission_classes = [IsDoctorOrGeneralManager]
    
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id)
        
        # Check permissions for doctors
        if request.user.role == 'DR' and patient not in request.user.doctor.patients.all():
            return Response({'error': 'You don\'t have access to this patient'}, 
                           status=status.HTTP_403_FORBIDDEN)
        
        recommendations = TreatmentRecommendation.objects.filter(patient=patient)
        applications = TreatmentApplication.objects.filter(patient=patient)
        
        return Response({
            'patient': PatientSerializer(patient).data,
            'recommendations': TreatmentRecommendationSerializer(recommendations, many=True).data,
            'applications': TreatmentApplicationSerializer(applications, many=True).data
        })
