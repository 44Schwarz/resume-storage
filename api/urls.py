from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'cvs', views.ResumeViewSet)
router.register(r'skills', views.SkillViewSet)
router.register(r'experiences', views.ExperienceViewSet)
router.register(r'companies', views.CompanyViewSet)
router.register(r'upload', views.UploadViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
