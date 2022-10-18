from rest_framework import serializers

from examination_management.student.models import Student
from examination_management.semester.api.v1.serializers import SemesterInstanceSerializer

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class StudentDetailSerializer(serializers.ModelSerializer):
    batch = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()
    semester_instance = SemesterInstanceSerializer(many=True, read_only=True, source='student_semester_instance')

    def get_batch(self, student):
        return str(student.batch.start)

    def get_branch(self, student):
        return str(student.branch.code)

    class Meta:
        model = Student
        fields = '__all__'
