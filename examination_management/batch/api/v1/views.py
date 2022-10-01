from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from examination_management.batch.api.v1.serializers import BatchSerializer
from examination_management.batch.models import Batch


class BatchCreateView(GenericAPIView):
    serializer_class = BatchSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        batch = Batch.objects.create(**validated_data)

        response = {
            'error': False,
            'data': self.get_serializer(batch).data
        }

        return Response(response, status=status.HTTP_201_CREATED)


class BatchDetailView(GenericAPIView):
    serializer_class = BatchSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, id=None):
        batch = Batch.objects.get(id=id)

        if not batch:
            response = {
                'error': True,
                'message': f'Batch with {id} not found!'
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'error': False,
            'data': self.get_serializer(batch).data
        }
        return Response(response, status=status.HTTP_200_OK)


class BatchListView(GenericAPIView):
    serializer_class = BatchSerializer
    queryset = Batch.objects.all()
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        batches = self.get_queryset()

        response = {
            'error': False,
            'data': self.get_serializer(batches, many=True).data
        }

        return Response(response, status=status.HTTP_200_OK)


class BatchUpdateView(GenericAPIView):
    serializer_class = BatchSerializer
    permission_classes = [permissions.AllowAny]

    def patch(self, request, id=None):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        batch = Batch.objects.get(id=id)
        if not batch:
            response = {
                'error': True,
                'message': f'Batch with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        batch = batch.update(**validated_data)
        response = {
            'error': False,
            'data': self.get_serializer(batch).data
        }
        return Response(response, status=status.HTTP_200_OK)


class BatchDeleteView(GenericAPIView):
    serializer_class = BatchSerializer
    permission_classes = [permissions.AllowAny]

    def delete(self, request, id=None):
        batch = Batch.objects.get(id=id)

        if not batch:
            response = {
                'error': True,
                'message': f'Batch with {id} not found!'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        batch.is_deleted = True
        batch.save()

        response = {
            'error': False,
            'message': f'Batch with {id} successfully deleted!'
        }
        return Response(response, status=status.HTTP_200_OK)