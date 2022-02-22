from dataclasses import field
from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Project, Contributor


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        field = (
            "title",
            "description",
            "type",
            "contributor_id",
        )
