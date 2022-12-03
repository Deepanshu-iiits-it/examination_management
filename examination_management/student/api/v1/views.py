import tempfile
from collections import OrderedDict

from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template

from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from examination_management.semester.models import SemesterInstance
from examination_management.grade.models import Grade
from examination_management.batch.models import Batch
from examination_management.branch.models import Branch
from examination_management.subject.models import Subject
from examination_management.student.api.v1.serializers import StudentSerializer, StudentDetailSerializer
from examination_management.student.models import Student, SerialNo
from examination_management.utils.utils import create_empty_excel, create_result_excel, get_roman


def _get_semester_data(semester, branch, batch):
    subjects = {}
    subject_instances = Subject.objects.filter(subject_semester__semester=semester)
    core_credit = 0
    for subject in subject_instances.all():
        subjects[subject.code] = {
            'name': subject.name,
            'code': subject.code,
            'credit': subject.credit
        }
        if not subject.is_elective:
            core_credit += subject.credit

    students = OrderedDict()
    students_instances = Student.objects.filter(student_semester_instance__semester__semester=semester,
                                                branch__code=branch, batch__start=batch)
    for student in students_instances.all():
        # For current semester
        semester_instance = SemesterInstance.objects.get(student__roll_no=student.roll_no,
                                                         semester__semester=semester)
        credit = 0
        for subject in semester_instance.semester.subject.all():
            if not subject.is_elective:
                credit += subject.credit
        for elective in semester_instance.elective.all():
            credit += elective.credit
        sgpa = round(semester_instance.cg_sum / credit, 4)

        grades = OrderedDict()
        reappear = []
        grade_instances = Grade.objects.filter(semester_instance=semester_instance.id)
        for grade in grade_instances.all():
            grades[grade.subject.code] = {
                'grade': grade.grade,
                'score': grade.score
            }

            if grade.grade and grade.grade >= 'F':
                reappear.append(grade.subject.code)
        reappear = ','.join(reappear)

        for subject in subject_instances.all():
            if not grades.get(subject.code, None):
                grades[subject.code] = {
                    'grade': '',
                    'score': 0
                }
        students[student.roll_no] = {
            'name': student.name,
            'fathers_name': student.fathers_name,
            'roll_no': student.roll_no,
            'grades': grades,
            'total_credit': credit,
            'cg_sum': semester_instance.cg_sum,
            'sgpa': sgpa,
            'reappear': reappear,
        }

        if semester > 4:
            # For previous semesters
            semester_instances = SemesterInstance.objects.filter(student__roll_no=student.roll_no)
            prev_semesters = {}
            total_credits = 0
            cgpa = 0
            for semester_instance in semester_instances:
                curr_credit = 0
                sem_no = semester_instance.semester.semester
                if sem_no > semester:
                    continue
                for subject in semester_instance.semester.subject.all():
                    if not subject.is_elective:
                        curr_credit += subject.credit
                for elective in semester_instance.elective.all():
                    curr_credit += elective.credit
                total_credits += curr_credit

                sgpa = round(semester_instance.cg_sum / curr_credit, 4)
                cgpa += sgpa
                year = batch + sem_no // 2
                prev_semesters[sem_no] = {
                    'session': f'Nov./Dec., {year}' if sem_no % 2 else f'May./June., {year}',
                    'roman_sem': get_roman(sem_no),
                    'credit': curr_credit,
                    'sgpa': sgpa,
                }

            students[student.roll_no]['prev_semesters'] = sorted(prev_semesters.items())
            students[student.roll_no]['total_credits'] = total_credits
            students[student.roll_no]['cgpa'] = round(cgpa / semester, 4)

    return subjects, students


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
            response = HttpResponse(fp,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
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

        subjects, students = _get_semester_data(semester, branch, batch)

        xlsx_name = f'Result Sheet {semester} Semester Batch {batch_instance.start}-{batch_instance.end}'
        with tempfile.NamedTemporaryFile(prefix=xlsx_name, suffix='.xlsx') as fp:
            create_result_excel(fp.name, subjects, students, semester, branch_name, batch_instance.start,
                                batch_instance.end)
            fp.seek(0)
            response = HttpResponse(fp,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={xlsx_name}.xlsx'
            return response


class StudentDMCDownloadView(GenericAPIView):
    def get(self, request):
        semester = int(request.GET.get('student_semester_instance__semester__semester', None))
        branch = request.GET.get('branch__code', None)
        batch = int(request.GET.get('batch__start', None))

        if not (semester and branch and batch):
            return HttpResponseRedirect('../')

        subjects, students = _get_semester_data(semester, branch, batch)

        serialno = SerialNo.objects.filter()[0]
        serial_no = serialno.serial_no
        new_serial_no = serial_no + len(students)
        # print(serial_no, new_serial_no)
        serialno.serial_no = new_serial_no
        serialno.save()

        title = f'DMC Semester {semester} Branch {branch} Batch {batch}.pdf'
        full_branch = Branch.objects.get(code=branch).branch
        year = batch + semester // 2

        if semester <= 4:
            template_path = 'student/dmc/student_dmc_till_4_sem_template.html'
        else:
            template_path = 'student/dmc/student_dmc_after_4_sem_template.html'
        context = {
            'subjects': sorted(subjects.items()),
            'students': students,
            'title': title,
            'branch': full_branch,
            'semester': get_roman(semester),
            'session': f'Nov./Dec., {year}' if semester % 2 else f'May./June., {year}',
            'serialno': serial_no,
        }
        template = get_template(template_path)

        return HttpResponse(template.render(context))
