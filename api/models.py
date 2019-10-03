import os

from django.db import models


# Create your models here.
class CV(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    about = models.TextField(blank=True)
    skill = models.ManyToManyField('Skill', blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Experience(models.Model):
    company = models.ForeignKey('Company', on_delete=models.PROTECT)
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    resume = models.ForeignKey(CV, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.company} ({self.date_start} - {self.date_end})'


class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# TODO build a relation between CV files and CV objects
class Upload(models.Model):
    cv_file = models.FileField(upload_to='cvs')

    def __str__(self):
        return os.path.basename(self.cv_file.name)
