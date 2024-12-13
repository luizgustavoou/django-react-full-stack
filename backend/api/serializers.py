from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Course, Note, Student

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
            model = Note
            fields = ["id", "title", "content", "created_at", "author"]
            extra_kwargs = {"author": {"read_only": True}}


class CourseSerializar(serializers.ModelSerializer):
     students = UserSerializer(many=True, read_only=True)
     class Meta:
          model = Course
          fields = ["id", "title", "description", "created_at", "students"]
          extra_kwargs = {"students": {"read_only": True}}

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "user", "course", "created_at"]
        extra_kwargs = {"user": {"read_only": True}, "course": {"read_only": True}}