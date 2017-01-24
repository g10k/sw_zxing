# coding=utf-8
from django.http import JsonResponse
from rest_framework.decorators import api_view
import zxing
from django.conf import settings
from PIL import Image
import tempfile
import shutil

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
    raw_text = ''

    if barcode:
        raw_text = barcode.raw
    else:
        _, tmp_path_jpeg_original = tempfile.mkstemp(suffix='.jpg')

        # /tmp/tmpcLDOaX.upload переименуем в /tmp/tmpcLDOaX.jpeg
        shutil.copy(file_obj.temporary_file_path(), tmp_path_jpeg_original)

        for degrees in [30, 60]:
            # Крутим на degrees градусов
            _, tmp_path = tempfile.mkstemp(suffix='.jpg')
            tmp_img_object = Image.open(tmp_path_jpeg_original).rotate(degrees).save(tmp_path)
            barcode = reader.decode(tmp_path, try_harder=True, qr_only=False)
            if barcode:
                raw_text = barcode.raw
                break
    return JsonResponse({'text': raw_text})