import tempfile

from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from examination_management.utils.utils import create_empty_excel
from examination_management.subject.api.v1.serializers import SubjectSerializer
from examination_management.subject.models import Subject


class SubjectCreateView(GenericAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        subject = Subject.objects.create(**validated_data)

        response = {
            'error': False,
            'data': self.get_serializer(subject).data
        }

        return Response(response, status=status.HTTP_201_CREATED)


class SubjectDetailView(GenericAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, id=None):
        subject = Subject.objects.get(id=id)

        if not subject:
            response = {
                'error': True,
                'message': f'Subject with {id} not found!'
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'error': False,
            'data': self.get_serializer(subject).data
        }
        return Response(response, status=status.HTTP_200_OK)


class SubjectListView(GenericAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code', None)
        # batch = request.GET.get('batch', None)
        # branch = request.GET.get('branch', None)

        queryset = self.get_queryset()
        subjects = queryset
        if code:
            subjects = queryset.filter(code=code)

        response = {
            'error': False,
            'data': self.get_serializer(subjects, many=True).data
        }

        return Response(response, status=status.HTTP_200_OK)


class SubjectUpdateView(GenericAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]

    def patch(self, request, id=None):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        subject = Subject.objects.get(id=id)
        if not subject:
            response = {
                'error': True,
                'message': f'Subject with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        subject = subject.update(**validated_data)
        response = {
            'error': False,
            'data': self.get_serializer(subject).data
        }
        return Response(response, status=status.HTTP_200_OK)


class SubjectDeleteView(GenericAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, id=None):
        subject = Subject.objects.get(id=id)

        if not subject:
            response = {
                'error': True,
                'message': f'Subject with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        subject.is_deleted = True
        subject.save()

        response = {
            'error': False,
            'message': f'Subject with {id} successfully deleted!'
        }
        return Response(response, status=status.HTTP_200_OK)


class SubjectTemplateDownloadView(GenericAPIView):

    def get(self, request):
        with tempfile.NamedTemporaryFile(prefix=f'Subject', suffix='.xlsx') as fp:
            create_empty_excel(path=fp.name, columns=['code', 'name', 'credit', 'is_elective'])
            fp.seek(0)
            response = HttpResponse(fp, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=Subject.xlsx'
            return response