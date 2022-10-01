
from django.urls import path

from examination_management.semester.api.v1.view import *

urlpatterns = [
    path('v1/create/',  view=SemesterCreateView.as_view(), name='semester_create'),
    path('v1/<int:id>/',  view=SemesterDetailView.as_view(), name='semester_fetch'),
    path('v1/list/',  view=SemesterListView.as_view(), name='semester_list'),
    path('v1/<int:id>/udpate/',  view=SemesterUpdateView.as_view(), name='semester_update'),
    path('v1/<int:id>/delete/',  view=SemesterDeleteView.as_view(), name='semester_delete'),

    path('instance/v1/create/',  view=SemesterInstanceCreateView.as_view(), name='semester_instance_create'),
    path('instance/v1/<int:id>/',  view=SemesterInstanceDetailView.as_view(), name='semester_instance_fetch'),
    path('instance/v1/list/',  view=SemesterInstanceListView.as_view(), name='semester_instance_list'),
    path('instance/v1/<int:id>/udpate/',  view=SemesterInstanceUpdateView.as_view(), name='semester_instance_update'),
    path('instance/v1/<int:id>/delete/',  view=SemesterInstanceDeleteView.as_view(), name='semester_instance_delete'),
]