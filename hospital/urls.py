from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import LoginView

router = DefaultRouter()
router.register(r'doctors', views.DoctorViewSet)
router.register(r'assistants', views.AssistantViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'treatments', views.TreatmentViewSet)
router.register(r'treatment-recommendations', views.TreatmentRecommendationViewSet)
router.register(r'treatment-applications', views.TreatmentApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('patient-assignments/', views.PatientAssignmentView.as_view(), name='patient-assignments'),
    path('reports/doctors-patients/', views.DoctorPatientsReportView.as_view(), name='doctors-patients-report'),
    path('reports/patient-treatments/<int:patient_id>/', views.PatientTreatmentsReportView.as_view(), name='patient-treatments-report'),
]

from rest_framework.authtoken import views

urlpatterns += [
    path('api/token-auth/', views.obtain_auth_token, name='api_token_auth'),
]
