import tempfile

from django.http import HttpResponse
from rest_framework.generics import GenericAPIView
from examination_management.utils.utils import create_empty_excel


class BranchTemplateDownloadView(GenericAPIView):

    def get(self, request):
        with tempfile.NamedTemporaryFile(prefix='Branch', suffix='.xlsx') as fp:
            create_empty_excel(path=fp.name, columns=['branch', 'code'])
            fp.seek(0)
            response = HttpResponse(fp, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=Branch.xlsx'
            return response
