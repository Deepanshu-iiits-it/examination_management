import tempfile

from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from examination_management.grade.api.v1.serializers import GradeSerializer
from examination_management.grade.models import Grade
from examination_management.semester.models import SemesterInstance
from examination_management.subject.models import Subject
from examination_management.utils.utils import create_excel


class GradeCreateView(GenericAPIView):
    serializer_class = GradeSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        grade = Grade.objects.create(**validated_data)

        response = {
            'error': False,
            'data': self.get_serializer(grade).data
        }

        return Response(response, status=status.HTTP_201_CREATED)


class GradeDetailView(GenericAPIView):
    serializer_class = GradeSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, id=None):
        grade = Grade.objects.get(id=id)

        if not grade:
            response = {
                'error': True,
                'message': f'Grade with {id} not found!'
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'error': False,
            'data': self.get_serializer(grade).data
        }
        return Response(response, status=status.HTTP_200_OK)


class GradeListView(GenericAPIView):
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        grade = request.GET.get('grade', None)
        # batch = request.GET.get('batch', None)
        # branch = request.GET.get('branch', None)

        queryset = self.get_queryset()
        grades = queryset
        if grade:
            grades = queryset.filter(grade=grade)

        response = {
            'error': False,
            'data': self.get_serializer(grades, many=True).data
        }

        return Response(response, status=status.HTTP_200_OK)


class GradeUpdateView(GenericAPIView):
    serializer_class = GradeSerializer
    permission_classes = [permissions.AllowAny]

    def patch(self, request, id=None):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        grade = Grade.objects.get(id=id)
        if not grade:
            response = {
                'error': True,
                'message': f'Grade with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        grade = grade.update(**validated_data)
        response = {
            'error': False,
            'data': self.get_serializer(grade).data
        }
        return Response(response, status=status.HTTP_200_OK)


class GradeDeleteView(GenericAPIView):
    serializer_class = GradeSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, id=None):
        grade = Grade.objects.get(id=id)

        if not grade:
            response = {
                'error': True,
                'message': f'Grade with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        grade.is_deleted = True
        grade.save()

        response = {
            'error': False,
            'message': f'Grade with {id} successfully deleted!'
        }
        return Response(response, status=status.HTTP_200_OK)


class GradeTemplateDownloadView(GenericAPIView):

    def get(self, request):
        semester = int(request.GET.get('semester_instance__semester__semester', None))
        branch = request.GET.get('semester_instance__student__branch__code', None)
        batch = int(request.GET.get('semester_instance__student__batch__start', None))
        subject = request.GET.get('subject__code', None)
        if not (semester and branch and batch and subject):
            return HttpResponseRedirect('../')

        subject_instance = Subject.objects.get(code=subject)
        if not subject_instance.is_elective:
            semester_instances = SemesterInstance.objects.filter(semester__semester=semester,
                                                                 student__batch__start=batch,
                                                                 student__branch__code=branch)
        else:
            semester_instances = SemesterInstance.objects.filter(semester__semester=semester,
                                                                 student__batch__start=batch,
                                                                 student__branch__code=branch,
                                                                 elective=subject_instance)

        students = []
        semester_instances_id = []
        subjects = []
        grades = []
        for semester_instance in semester_instances:
            students.append(semester_instance.student.roll_no)
            semester_instances_id.append(semester_instance.id)
            subjects.append(subject)
            grades.append('')

        data = {
            'student': students,
            'semester_instance': semester_instances_id,
            'subject': subjects,
            'grade': grades
        }

        with tempfile.NamedTemporaryFile(prefix=f'{subject} grade sheet', suffix='.xlsx') as fp:
            create_excel(path=fp.name, data=data)
            fp.seek(0)
            response = HttpResponse(fp,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={subject} grade sheet.xlsx'
            return response
