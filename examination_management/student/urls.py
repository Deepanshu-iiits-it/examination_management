
from django.urls import path

from examination_management.student.api.v1.views import *

urlpatterns = [
    path('v1/create/',  view=StudentCreateView.as_view(), name='student_create'),
    path('v1/<int:id>/',  view=StudentDetailView.as_view(), name='student_fetch'),
    path('v1/list/',  view=StudentListView.as_view(), name='student_list'),
    path('v1/<int:id>/udpate/',  view=StudentUpdateView.as_view(), name='student_update'),
    path('v1/<int:id>/delete/',  view=StudentDeleteView.as_view(), name='student_delete'),
]