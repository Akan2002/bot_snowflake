from rest_framework.routers import DefaultRouter as DR

from mainapp.views import (
    ProjectView, ApplicationView
)

router = DR()

router.register('project', ProjectView, basename='project')
router.register('application', ApplicationView, basename='application')

urlpatterns = []

urlpatterns += router.urls