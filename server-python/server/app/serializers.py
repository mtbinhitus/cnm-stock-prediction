from rest_framework import serializers
from app.models import Endpoint
from app.models import MLModel
from app.models import MLModelStatus
from app.models import MLRequest


# read_only_fields: các trường chỉ cho phép đọc

class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        read_only_fields = ("id", "name", "owner", "created_at")
        fields = read_only_fields


class MLModelSerializer(serializers.ModelSerializer):

    current_status = serializers.SerializerMethodField(read_only=True)

    def get_current_status(self, mlmodel):
        return MLModelStatus.objects.filter(parent_mlmodel=mlmodel).latest('created_at').status

    class Meta:
        model = MLModel
        read_only_fields = ("id", "name", "description", "version",
                            "owner", "created_at", "parent_endpoint", "current_status")
        fields = read_only_fields


class MLModelStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModelStatus
        read_only_fields = ("id", "active")
        fields = ("id", "active", "status", "created_by",
                  "created_at", "parent_mlmodel")


class MLRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLRequest
        read_only_fields = (
            "id",
            "input_data",
            "full_response",
            "response",
            "created_at",
            "parent_mlmodel",
        )
        fields = (
            "id",
            "input_data",
            "full_response",
            "response",
            "feedback",
            "created_at",
            "parent_mlmodel",
        )
