import os
from selenium import webdriver
import sys
import subprocess
import signal

def before_all(context):
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sys.path.append(path) # we need this so python can find our app as a module
    os.environ["DJANGO_SETTINGS_MODULE"] = "hsabackend.settings"
    context.url = "http://localhost:4200"
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../HSA-frontend'))
    os.chdir(path)
    context.angular = subprocess.Popen(["ng", "serve"])
    context.browser = webdriver.Chrome()

def after_all(context):
    context.angular.send_signal(signal.SIGINT)
    context.angular.wait()