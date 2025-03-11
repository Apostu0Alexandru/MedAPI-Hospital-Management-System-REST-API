from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import LoginView
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'doctors', views.DoctorViewSet)
router.register(r'assistants', views.AssistantViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'treatments', views.TreatmentViewSet)
router.register(r'treatment-recommendations', views.TreatmentRecommendationViewSet)
router.register(r'treatment-applications', views.TreatmentApplicationViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Hospital Management API",
      default_version='v1',
      description="API for hospital management system with role-based access (GM, Doctor, Assistant)",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('patient-assignments/', views.PatientAssignmentView.as_view(), name='patient-assignments'),
    path('reports/doctors-patients/', views.DoctorPatientsReportView.as_view(), name='doctors-patients-report'),
    path('reports/patient-treatments/<int:patient_id>/', views.PatientTreatmentsReportView.as_view(), name='patient-treatments-report'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

from rest_framework.authtoken import views

urlpatterns += [
    path('api/token-auth/', views.obtain_auth_token, name='api_token_auth'),
]
