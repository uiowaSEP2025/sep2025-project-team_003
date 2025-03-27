import subprocess
import time
import os
import requests
from requests.exceptions import ConnectionError
import time
from selenium import webdriver

def block_until_server_is_up(url, timeout=30, interval=2):
    """Block untill the server is up."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.ok:
                print("angular was started successfully!!")
                return True
        except ConnectionError:
            pass
        time.sleep(interval)
    return False

def before_all(context):
    """If runing on CICD ```behave -D CI=True```"""
    context.is_CI = context.config.userdata.get("CI", False)
    context.is_dev = context.config.userdata.get("DEV", False) # if the integration tests are being ran against dev
    context.browser = webdriver.Chrome()
    context.url = "http://localhost:4200" if not context.is_dev else "FIX IT PLEASE"

    if context.is_CI:
        pass
    else:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../HSA-frontend')) # frontend to do ng serve
        os.chdir(path)
        context.angular_process = subprocess.Popen(["ng", "serve", "--port", "4200"])
        block_until_server_is_up("http://localhost:4200")
        
        if context.angular_process.poll() is not None:
            error_message = "Angular server failed to start. \n"
            if context.server_process.returncode == 0:
                error_message += "Process exited successfully but shouldn't have.\n"
            else:
                error_message += f"Process exited with return code {context.server_process.returncode} \n"
            raise RuntimeError(error_message)


def after_all(context):
    if context.is_CI:
        pass
    else:
        context.angular_process.terminate()
