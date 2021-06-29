from django.shortcuts import render

# Create your views here.
import swarm.monitor.templates
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
import datetime
from django.db.models import Max
import MySQLdb
import json
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import logging
import threading
import time
import os
import sys
import configparser
from django.db import connection


def index(request):
    t = loader.get_template("index.html")
    c = {}
    return HttpResponse(t.render(c))


def add_nodes(request):
    file_path = request.GET.get('filePath')
    print(file_path)
    file = open(file_path, 'r')
    context = file.read()
    print('read格式:')
    print(context)
    file.close()

    nodes = {}
    ret = {'code': 0, 'msg': '', 'result': {'nodes': nodes}}
    ret_json = json.dumps(ret)
    return HttpResponse(ret_json)
