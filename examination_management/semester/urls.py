
from django.urls import path

from examination_management.semester.api.v1.view import *

urlpatterns = [
    path('v1/create/',  view=SemesterCreateView.as_view(), name='semester_create'),
    path('v1/<int:id>/',  view=SemesterDetailView.as_view(), name='semester_fetch'),
    path('v1/list/',  view=SemesterListView.as_view(), name='semester_list'),
    path('v1/<int:id>/udpate/',  view=SemesterUpdateView.as_view(), name='semester_update'),
    path('v1/<int:id>/delete/',  view=SemesterDeleteView.as_view(), name='semester_delete'),
]