
from django.urls import path

from examination_management.subject.api.v1.views import *

urlpatterns = [
    path('v1/create/',  view=SubjectCreateView.as_view(), name='subject_create'),
    path('v1/<int:id>/',  view=SubjectDetailView.as_view(), name='subject_fetch'),
    path('v1/list/',  view=SubjectListView.as_view(), name='subject_list'),
    path('v1/<int:id>/udpate/',  view=SubjectUpdateView.as_view(), name='subject_update'),
    path('v1/<int:id>/delete/',  view=SubjectDeleteView.as_view(), name='subject_delete'),
]