
from django.urls import path

from examination_management.grade.api.v1.views import *

urlpatterns = [
    path('v1/create/',  view=GradeCreateView.as_view(), name='grade_create'),
    path('v1/<int:id>/',  view=GradeDetailView.as_view(), name='grade_fetch'),
    path('v1/list/',  view=GradeListView.as_view(), name='grade_list'),
    path('v1/<int:id>/udpate/',  view=GradeUpdateView.as_view(), name='grade_update'),
    path('v1/<int:id>/delete/',  view=GradeDeleteView.as_view(), name='grade_delete'),
]