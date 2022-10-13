from rest_framework import serializers

from examination_management.student.models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class StudentDetailSerializer(serializers.ModelSerializer):
    batch = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()

    def get_batch(self, student):
        return str(student.batch.start)

    def get_branch(self, student):
        return str(student.branch.code)

    class Meta:
        model = Student
        fields = '__all__'