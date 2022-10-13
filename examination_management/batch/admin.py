from django.contrib import admin

from examination_management.batch.models import Batch


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    model = Batch
