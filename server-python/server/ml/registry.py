from app.models import Endpoint
from app.models import MLModel
from app.models import MLModelStatus


class MLRegistry:
    def __init__(self):
        self.endpoints = {}

    def add_algorithm(self, endpoint_name, algorithm_object, algorithm_name,
                      algorithm_status, algorithm_version, owner,
                      algorithm_description):
        # get endpoint
        endpoint, _ = Endpoint.objects.get_or_create(
            name=endpoint_name, owner=owner)

        # get model algorithm
        database_object, algorithm_created = MLModel.objects.get_or_create(
            name=algorithm_name,
            description=algorithm_description,
            version=algorithm_version,
            owner=owner,
            parent_endpoint=endpoint)
        if algorithm_created:
            status = MLModelStatus(status=algorithm_status,
                                   created_by=owner,
                                   parent_mlmodel=database_object,
                                   active=True)
            status.save()

        # add to registry
        self.endpoints[database_object.id] = algorithm_object