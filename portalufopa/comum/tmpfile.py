# -*- coding: UTF-8 -*-
import datetime
import glob
import os


#from django.conf import settings
def __teste_directory_exist(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def create_file_tmp(user_id):
    file_name = (datetime.datetime.now()-datetime.datetime(1970,1,1)).total_seconds()
    file_name = 'tmp/%s_%s.%s.tmp' % (user_id, file_name, os.getpid())
    __teste_directory_exist('tmp/')
    try:
        with open(file_name, 'w+b') as tmp:
            tmp.write('ReadFile - TMP, create date %s. ' % datetime.date.today())
    except:
        pass
        
    return file_name

def write_reaf_file_tmp(file_name, content):
    with open(file_name, 'w+b') as tmp:
        tmp.write(content)

def delete_file_tmp(user_id):
    file_name = 'tmp/%s*.tmp' % user_id
    for f in glob.glob(file_name):
        os.remove(f)
