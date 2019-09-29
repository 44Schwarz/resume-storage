from rest_framework import viewsets, filters

from .models import CV, Skill, Experience, Company, Upload
from .serializers import CVSerializer, SkillSerializer, ExperienceSerializer, CompanySerializer, UploadSerializer


# Create your views here.
class ResumeViewSet(viewsets.ModelViewSet):
    queryset = CV.objects.all().order_by('id')
    serializer_class = CVSerializer

    filter_backends = (filters.SearchFilter, )
    search_fields = ('skill__name', 'experience__company__name')  # TODO search by company name is enough?


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().order_by('id')
    serializer_class = SkillSerializer


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all().order_by('id')
    serializer_class = ExperienceSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('id')
    serializer_class = CompanySerializer


class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all().order_by('id')
    serializer_class = UploadSerializer
