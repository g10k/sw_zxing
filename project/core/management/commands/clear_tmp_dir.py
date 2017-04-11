# coding: utf-8
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import shutil
import time
import datetime


def _clear_tmp_dir(folder):
    now = datetime.datetime.now()
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        modify_date = datetime.datetime.fromtimestamp(os.stat(file_path).st_mtime)
        old = now - modify_date
        if old.total_seconds() < 60:
            continue
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


class Command(BaseCommand):
    help = u'Ощичаем директорию /tmp каждый час'


    def add_arguments(self, parser):
        parser.add_argument('--one-shot',action='store_true', dest='one_shot', default=False,help=u'Выполнить один раз')

    def handle(self, *args, **options):

        print options.get('one_shot')

        if options.get('one_shot'):
            _clear_tmp_dir('/tmp/')
        else:
            while True:
                _clear_tmp_dir('/tmp/')
                time.sleep(10)