#-*- encoding: utf-8 -*-
__author__ = 'brian'
import os
from configuracion.settings import PROJECT_PATH
def copiabd():
    print "copiando base de datos"
    os.system("cp /home/brian/Webs/webdreamsappscreative/accesoDAC/dbsqlite /home/brian/Webs/webdreamsappscreative/accesoDAC/dbsqlite_backup")


