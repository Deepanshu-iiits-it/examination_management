import tempfile

from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from examination_management.semester.api.v1.serializers import *
from examination_management.semester.models import Semester, SemesterInstance

from examination_management.utils.utils import create_empty_excel


class SemesterCreateView(GenericAPIView):
    serializer_class = SemesterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        semester = Semester.objects.create(**validated_data)

        response = {
            'error': False,
            'data': self.get_serializer(semester).data
        }

        return Response(response, status=status.HTTP_201_CREATED)


class SemesterDetailView(GenericAPIView):
    serializer_class = SemesterSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, id=None):
        semester = Semester.objects.get(id=id)

        if not semester:
            response = {
                'error': True,
                'message': f'Semester with {id} not found!'
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'error': False,
            'data': self.get_serializer(semester).data
        }
        return Response(response, status=status.HTTP_200_OK)


class SemesterListView(GenericAPIView):
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        semester = queryset

        response = {
            'error': False,
            'data': self.get_serializer(semester, many=True).data
        }

        return Response(response, status=status.HTTP_200_OK)


class SemesterUpdateView(GenericAPIView):
    serializer_class = SemesterSerializer
    permission_classes = [permissions.AllowAny]

    def patch(self, request, id=None):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        semester = Semester.objects.get(id=id)
        if not semester:
            response = {
                'error': True,
                'message': f'Semester with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        semester = semester.update(**validated_data)
        response = {
            'error': False,
            'data': self.get_serializer(semester).data
        }
        return Response(response, status=status.HTTP_200_OK)


class SemesterDeleteView(GenericAPIView):
    serializer_class = SemesterSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, id=None):
        semester = Semester.objects.get(id=id)

        if not semester:
            response = {
                'error': True,
                'message': f'Semester with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        semester.is_deleted = True
        semester.save()

        response = {
            'error': False,
            'message': f'Semester with {id} successfully deleted!'
        }
        return Response(response, status=status.HTTP_200_OK)


class SemesterInstanceCreateView(GenericAPIView):
    serializer_class = SemesterInstanceSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        student = validated_data['student']

        # Check if the student has an active semester
        if len(student.student_semester_instance.all()) > 0:
            for sem_instance in student.student_semester_instance.all():
                if sem_instance.status == 'A':
                    response = {
                        'error': True,
                        'message': 'A student cannot be registered for multiple semesters!'
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)

        semester_instance = SemesterInstance.objects.create(**validated_data)
        response = {
            'error': False,
            'data': SemesterInstanceDetailSerializer(semester_instance).data
        }
        return Response(response, status=status.HTTP_201_CREATED)


class SemesterInstanceDetailView(GenericAPIView):
    serializer_class = SemesterInstanceDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, id=None):
        try:
            semester_instance = SemesterInstance.objects.get(id=id)

            if not semester_instance:
                response = {
                    'error': True,
                    'message': f'Semester Instance with {id} not found!'
                }

                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            response = {
                'error': False,
                'data': self.get_serializer(semester_instance).data
            }
            return Response(response, status=status.HTTP_200_OK)

        # TODO: Remove wide except
        except:
            response = {
                'error': True,
                'message': f'Semester Instance with {id} does not exist!'
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class SemesterInstanceListView(GenericAPIView):
    serializer_class = SemesterInstanceDetailSerializer
    queryset = SemesterInstance.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        roll_no = request.GET.get('roll_no', None)

        # TODO: Add more filters
        # batch = request.GET.get('batch', None)
        # branch = request.GET.get('branch', None)

        queryset = self.get_queryset()
        semester = queryset
        if roll_no:
            semester = queryset.filter(roll_no=roll_no)

        response = {
            'error': False,
            'data': self.get_serializer(semester, many=True).data
        }

        return Response(response, status=status.HTTP_200_OK)


class SemesterInstanceUpdateView(GenericAPIView):
    serializer_class = SemesterInstanceSerializer
    permission_classes = [permissions.AllowAny]

    def patch(self, request, id=None):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        semester = SemesterInstance.objects.get(id=id)
        if not semester:
            response = {
                'error': True,
                'message': f'Semester with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        semester = semester.update(**validated_data)
        response = {
            'error': False,
            'data': SemesterInstanceDetailSerializer(semester).data
        }
        return Response(response, status=status.HTTP_200_OK)


class SemesterInstanceDeleteView(GenericAPIView):
    serializer_class = SemesterInstanceSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, id=None):
        semester = SemesterInstance.objects.get(id=id)

        if not semester:
            response = {
                'error': True,
                'message': f'Semester with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        semester.is_deleted = True
        semester.save()

        response = {
            'error': False,
            'message': f'Semester with {id} successfully deleted!'
        }
        return Response(response, status=status.HTTP_200_OK)


class SemesterInstanceTemplateDownloadView(GenericAPIView):

    def get(self, request):
        with tempfile.NamedTemporaryFile(prefix=f'Student Registration', suffix='.xlsx') as fp:
            create_empty_excel(path=fp.name, columns=['student', 'semester'])
            fp.seek(0)
            response = HttpResponse(fp, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=Semester Registration.xlsx'
            return response

