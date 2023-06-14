from rest_framework.viewsets import ModelViewSet

from mainapp.models import (
    Project, Application
)
from mainapp.serializer import (
    ProjectSerializer, ApplicationSerializer
)


class ProjectView(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ApplicationView(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
