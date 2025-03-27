from rest_framework import serializers
from .models import User, Doctor, Assistant, Patient, Treatment, TreatmentRecommendation, TreatmentApplication

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    assistants = serializers.PrimaryKeyRelatedField(many=True, read_only=True, queryset=Assistant.objects.all())
    
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization', 'department', 'assistants']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'DR'
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor

class AssistantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    assigned_doctors = DoctorSerializer(many=True, read_only=True)
    
    class Meta:
        model = Assistant
        fields = ['id', 'user', 'department', 'assigned_doctors']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'AS'
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        assistant = Assistant.objects.create(user=user, **validated_data)
        return assistant

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 
                 'address', 'phone_number', 'medical_history']

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ['id', 'name', 'description', 'cost']

class TreatmentRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentRecommendation
        fields = ['id', 'doctor', 'patient', 'treatment', 
                 'recommendation_date', 'notes']

class TreatmentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentApplication
        fields = ['id', 'assistant', 'patient', 'treatment', 
                 'application_date', 'status', 'notes']
