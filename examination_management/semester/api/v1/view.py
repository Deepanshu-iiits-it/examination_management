from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from examination_management.semester.api.v1.serializers import SemesterSerializer
from examination_management.semester.models import Semester


class SemesterCreateView(GenericAPIView):
    serializer_class = SemesterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        student = Semester.objects.create(**validated_data)

        response = {
            'error': False,
            'data': self.get_serializer(student).data
        }

        return Response(response, status=status.HTTP_201_CREATED)


class SemesterDetailView(GenericAPIView):
    serializer_class = SemesterSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, id=None):
        student = Semester.objects.get(id=id)

        if not student:
            response = {
                'error': True,
                'message': f'Semester with {id} not found!'
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'error': False,
            'data': self.get_serializer(student).data
        }
        return Response(response, status=status.HTTP_200_OK)


class SemesterListView(GenericAPIView):
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        roll_no = request.GET.get('roll_no', None)
        # batch = request.GET.get('batch', None)
        # branch = request.GET.get('branch', None)

        queryset = self.get_queryset()
        students = queryset
        if roll_no:
            students = queryset.filter(roll_no=roll_no)

        response = {
            'error': False,
            'data': self.get_serializer(students, many=True).data
        }

        return Response(response, status=status.HTTP_200_OK)


class SemesterUpdateView(GenericAPIView):
    serializer_class = SemesterSerializer
    permission_classes = [permissions.AllowAny]

    def patch(self, request, id=None):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        student = Semester.objects.get(id=id)
        if not student:
            response = {
                'error': True,
                'message': f'Semester with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        student = student.update(**validated_data)
        response = {
            'error': False,
            'data': self.get_serializer(student).data
        }
        return Response(response, status=status.HTTP_200_OK)


class SemesterDeleteView(GenericAPIView):
    serializer_class = SemesterSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, id=None):
        student = Semester.objects.get(id=id)

        if not student:
            response = {
                'error': True,
                'message': f'Semester with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        student.is_deleted = True
        student.save()

        response = {
            'error': False,
            'message': f'Semester with {id} successfully deleted!'
        }
        return Response(response, status=status.HTTP_200_OK)