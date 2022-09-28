from rest_framework import serializers

from examination_management.batch.models import Batch


class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'
