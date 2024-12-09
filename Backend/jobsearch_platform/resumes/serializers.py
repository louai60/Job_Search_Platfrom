from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'file', 'skills', 'experience', 'education', 'parsed_data']
        read_only_fields = ['skills', 'experience', 'education', 'parsed_data']
