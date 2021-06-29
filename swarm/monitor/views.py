from django.shortcuts import render

# Create your views here.
import monitor.templates
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
    t = loader.get_template("monitor/index.html")
    c = {}
    return HttpResponse(t.render(c))
