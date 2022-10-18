from rest_framework import serializers

from examination_management.semester.models import Semester, SemesterInstance
# from examination_management.student.api.v1.serializers import StudentSerializer


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'


class SemesterInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemesterInstance
        fields = '__all__'


class SemesterInstanceDetailSerializer(serializers.ModelSerializer):
    # TODO: Create Detail Serializers for both with necessary details
    semester = SemesterSerializer()
    # student = StudentSerializer()

    class Meta:
        model = SemesterInstance
        fields = '__all__'
