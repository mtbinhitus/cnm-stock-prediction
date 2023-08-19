from django.shortcuts import render
from django.db import transaction

from rest_framework import viewsets
from rest_framework import mixins

from app.models import Endpoint
from app.serializers import EndpointSerializer

from app.models import MLModel
from app.serializers import MLModelSerializer

from app.models import MLModelStatus
from app.serializers import MLModelStatusSerializer

from app.models import MLRequest
from app.serializers import MLRequestSerializer

# Create your views here.

class EndpointViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = EndpointSerializer
    queryset = Endpoint.objects.all()


class MLModelViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = MLModelSerializer
    queryset = MLModel.objects.all()


def deactivate_other_statuses(instance):
    old_statuses = MLModelStatus.objects.filter(parent_mlmodel=instance.parent_mlmodel,
                                                created_at__lt=instance.created_at,
                                                active=True)
    for i in range(len(old_statuses)):
        old_statuses[i].active = False
    MLModelStatus.objects.bulk_update(old_statuses, ["active"])


class MLModelStatusViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.CreateModelMixin
):
    serializer_class = MLModelStatusSerializer
    queryset = MLModelStatus.objects.all()

    # gọi bởi CreateModelMixin class để lưu một object mới
    def perform_create(self, serializer):
        try:
            # quản lý các tiến trình nhỏ trong Django transaction. Success thì active == True và ngược lại
            with transaction.atomic():
                instance = serializer.save(active=True)
                # set active=False for other statuses
                deactivate_other_statuses(instance)

        except Exception as e:
            raise APIException(str(e))


class MLRequestViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
    mixins.UpdateModelMixin
):
    serializer_class = MLRequestSerializer
    queryset = MLRequest.objects.all()
