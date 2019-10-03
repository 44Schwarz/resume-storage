from rest_framework import viewsets, filters

from .tasks import pdf_to_text

from .models import CV, Skill, Experience, Company, Upload
from .serializers import CVSerializer, SkillSerializer, ExperienceSerializer, CompanySerializer, UploadSerializer


# Create your views here.
class ResumeViewSet(viewsets.ModelViewSet):
    queryset = CV.objects.all().order_by('id')
    serializer_class = CVSerializer

    filter_backends = (filters.SearchFilter, )
    search_fields = ('skill__name', 'experience__company__name')


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

    def perform_create(self, serializer):
        new_obj = serializer.save()
        pdf_to_text.delay(new_obj.cv_file.path)

    def perform_update(self, serializer):
        new_obj = serializer.save()
        pdf_to_text.delay(new_obj.cv_file.path)
