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
    print 'post', request.POST
    print 'files', request.FILES
    print 'files:', request.FILES['filename']
    file_obj = request.FILES['filename']
    print 'file_obj: ', file_obj
    reader = zxing.BarCodeReader(settings.ZXING_PATH)
    print file_obj.temporary_file_path()
    barcode = reader.decode(file_obj.temporary_file_path(), try_harder=True, qr_only=False)
    raw_text = barcode.raw
    print "raw_text: ", raw_text
    return JsonResponse({'text': raw_text})