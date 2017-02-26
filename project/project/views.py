# coding=utf-8
import os
from django.http import JsonResponse
from rest_framework.decorators import api_view
import zxing
from django.conf import settings
from PIL import Image
import tempfile
import shutil
import re


def clear_tmp_dir(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


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

    if barcode and re.findall(r'\d{10}', barcode.raw):
        raw_text = barcode.raw
    else:
        _, tmp_path_jpeg_original = tempfile.mkstemp(suffix='.jpg')

        # сохраним файл в /tmp/tmpcLDOaX.jpeg
        shutil.copy(file_obj.temporary_file_path(), tmp_path_jpeg_original)

        for degrees in [30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]:
            _, tmp_path = tempfile.mkstemp(suffix='.jpg')
            tmp_img_object = Image.open(tmp_path_jpeg_original).rotate(degrees).save(tmp_path)
            barcode = reader.decode(tmp_path, try_harder=True, qr_only=False)
            if barcode and re.findall(r'\d{10}', barcode.raw):
                raw_text = barcode.raw
                break
    clear_tmp_dir(tempfile.gettempdir())
    return JsonResponse({'text': raw_text})
