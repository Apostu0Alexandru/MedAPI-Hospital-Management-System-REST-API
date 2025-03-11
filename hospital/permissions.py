from rest_framework import permissions

class IsGeneralManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'GM'

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'DR'
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'doctor'):
            return obj.doctor.user == request.user
        elif hasattr(obj, 'doctors'):
            return request.user.doctor in obj.doctors.all()
        return False

class IsAssistant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'AS'
    
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'assistant'):
            return obj.assistant.user == request.user
        elif hasattr(obj, 'assistants'):
            return request.user.assistant in obj.assistants.all()
        return False

class IsDoctorOrGeneralManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['DR', 'GM']
