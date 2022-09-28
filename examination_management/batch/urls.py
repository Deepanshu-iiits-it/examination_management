
from django.urls import path

from examination_management.batch.api.v1.views import *

urlpatterns = [
    path('v1/create/',  view=BatchCreateView.as_view(), name='batch_create'),
    path('v1/<int:id>/',  view=BatchDetailView.as_view(), name='batch_fetch'),
    path('v1/list/',  view=BatchListView.as_view(), name='batch_list'),
    path('v1/<int:id>/udpate/',  view=BatchUpdateView.as_view(), name='batch_update'),
    path('v1/<int:id>/delete/',  view=BatchDeleteView.as_view(), name='batch_delete'),
]