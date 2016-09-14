from django.http import JsonResponse
from rest_framework.decorators import api_view
import zxing
from django.conf import settings


@api_view(['post'])
def upload(request):
    '''
    ---

    parameters:
        - name: filename
          type: file
    '''
    file_obj = request.FILES['filename']
    reader = zxing.BarCodeReader(settings.ZXING_PATH)
    barcode = reader.decode(file_obj.temporary_file_path(), try_harder=True, qr_only=False)
    raw_text = barcode.raw if barcode else ''
    return JsonResponse({'text': raw_text})