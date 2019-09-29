from rest_framework import serializers

from .models import CV, Skill, Experience, Company


class SkillSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Skill
        fields = '__all__'


class CompanySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class ExperienceSerializer(serializers.HyperlinkedModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = Experience
        fields = '__all__'


class CVSerializer(serializers.HyperlinkedModelSerializer):
    skill = SkillSerializer(many=True, required=False)
    experiences = ExperienceSerializer(many=True, required=False, source='experience_set')

    class Meta:
        model = CV
        fields = '__all__'

    def create(self, validated_data):
        experience_data = validated_data.pop('experience_set', [])
        skills_data = validated_data.pop('skill', [])
        cv = CV.objects.create(**validated_data)

        for skill in skills_data:
            skill_obj, _ = Skill.objects.get_or_create(name=skill.get('name'))
            cv.skill.add(skill_obj)
            cv.save()

        for experience in experience_data:
            company_obj, _ = Company.objects.get_or_create(name=experience.get('company').get('name'))
            Experience.objects.update_or_create(company=company_obj, resume=cv,
                                                defaults={'date_start': experience.get('date_start'),
                                                          'date_end': experience.get('date_end'),
                                                          'description': experience.get('description')})

        return cv

    def update(self, instance, validated_data):
        experience_data = validated_data.pop('experience_set', [])
        skills_data = validated_data.pop('skill', [])

        if skills_data:
            instance.skill.clear()
        for skill in skills_data:
            skill_obj, _ = Skill.objects.get_or_create(name=skill.get('name'))
            instance.skill.add(skill_obj)
            instance.save()

        for experience in experience_data:
            company_obj, _ = Company.objects.get_or_create(name=experience.get('company').get('name'))
            Experience.objects.update_or_create(company=company_obj, resume=instance,
                                                defaults={'date_start': experience.get('date_start'),
                                                          'date_end': experience.get('date_end'),
                                                          'description': experience.get('description')})

        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.about = validated_data.get('about')

        instance.save()

        return instance
