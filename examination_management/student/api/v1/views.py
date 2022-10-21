import tempfile

from django.http import HttpResponse, HttpResponseRedirect

from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from examination_management.semester.models import SemesterInstance
from examination_management.grade.models import Grade
from examination_management.batch.models import Batch
from examination_management.branch.models import Branch
from examination_management.subject.models import Subject
from examination_management.student.api.v1.serializers import StudentSerializer, StudentDetailSerializer
from examination_management.student.models import Student
from examination_management.utils.utils import create_empty_excel, create_result_excel


class StudentCreateView(GenericAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        student = Student.objects.get_or_create(**validated_data)

        response = {
            'error': False,
            'data': self.get_serializer(student).data
        }

        return Response(response, status=status.HTTP_201_CREATED)


class StudentDetailView(GenericAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, id=None):
        student = Student.objects.get(id=id)

        if not student:
            response = {
                'error': True,
                'message': f'Student with {id} not found!'
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'error': False,
            'data': StudentDetailSerializer(student).data
        }
        return Response(response, status=status.HTTP_200_OK)


class StudentListView(GenericAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        roll_no = request.GET.get('roll_no', None)
        batch = request.GET.get('batch', None)
        branch = request.GET.get('branch', None)

        queryset = self.get_queryset()
        students = queryset
        if roll_no:
            students = queryset.filter(roll_no=roll_no)
        if batch:
            students = queryset.filter(batch__start=batch)
        if branch:
            students = queryset.filter(branch__code=branch)

        response = {
            'error': False,
            'data': StudentDetailSerializer(students, many=True).data
        }

        return Response(response, status=status.HTTP_200_OK)


class StudentUpdateView(GenericAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]

    def patch(self, request, id=None):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        student = Student.objects.get(id=id)
        if not student:
            response = {
                'error': True,
                'message': f'Student with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        student = student.update(**validated_data)
        response = {
            'error': False,
            'data': self.get_serializer(student).data
        }
        return Response(response, status=status.HTTP_200_OK)


class StudentDeleteView(GenericAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, id=None):
        student = Student.objects.get(id=id)

        if not student:
            response = {
                'error': True,
                'message': f'Student with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        student.is_deleted = True
        student.save()

        response = {
            'error': False,
            'message': f'Student with {id} successfully deleted!'
        }
        return Response(response, status=status.HTTP_200_OK)


class StudentTemplateDownloadView(GenericAPIView):

    def get(self, request):
        with tempfile.NamedTemporaryFile(prefix=f'Student Admission', suffix='.xlsx') as fp:
            create_empty_excel(path=fp.name, columns=['roll_no', 'name', 'fathers_name', 'email', 'batch', 'branch'])
            fp.seek(0)
            response = HttpResponse(fp, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=Student Admission.xlsx'
            return response


class StudentResultTemplateDownloadView(GenericAPIView):

    def get(self, request):
        semester = int(request.GET.get('student_semester_instance__semester__semester', None))
        branch = request.GET.get('branch__code', None)
        batch = int(request.GET.get('batch__start', None))

        if not (semester and branch and batch):
            return HttpResponseRedirect('../')

        branch_name = Branch.objects.get(code=branch)
        batch_instance = Batch.objects.get(start=batch)

        subjects = {}
        subject_instances = Subject.objects.filter(subject_semester__semester=semester)
        for subject in subject_instances.all():
            subjects[subject.code] = {
                'name': subject.name,
                'code': subject.code,
                'credit': subject.credit
            }

        students = {}
        students_instances = Student.objects.filter(student_semester_instance__semester__semester=semester,
                                                    branch__code=branch, batch__start=batch)
        for student in students_instances.all():
            semester_instance = SemesterInstance.objects.get(student__roll_no=student.roll_no, semester__semester=semester)
            sgpa = round(semester_instance.cg_sum / semester_instance.semester.credit, 4)

            grades = {}
            grade_instances = Grade.objects.filter(semester_instance=semester_instance.id)
            for grade in grade_instances.all():
                grades[grade.subject.code] = {
                    'grade': grade.grade,
                    'score': grade.score
                }

            subject_instances = semester_instance.semester.subject
            reappear = []
            for subject in subject_instances.all():
                if grades[subject.code]['grade'] >= 'F':
                    reappear.append(subject.code)
            reappear = ','.join(reappear)

            students[student.roll_no] = {
                'name': student.name,
                'fathers_name': student.fathers_name,
                'roll_no': student.roll_no,
                'grades': grades,
                'total_credit': semester_instance.semester.credit,
                'cg_sum': semester_instance.cg_sum,
                'sgpa': sgpa,
                'reappear': reappear
            }

        xlsx_name = f'Result Sheet {semester} Semester Batch {batch_instance.start}-{batch_instance.end}'
        with tempfile.NamedTemporaryFile(prefix=xlsx_name, suffix='.xlsx') as fp:
            create_result_excel(fp.name, subjects, students, semester, branch_name, batch_instance.start, batch_instance.end)
            fp.seek(0)
            response = HttpResponse(fp, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={xlsx_name}.xlsx'
            return response

