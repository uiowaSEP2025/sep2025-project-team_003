import subprocess
import time
import os

def before_all(context):
    """Start the Angular app before tests run."""
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../HSA-frontend')) # frontend to do ng serve
    os.chdir(path)
    context.server_process = subprocess.Popen(["ng", "serve", "--port", "4200"])
    time.sleep(5)  # Give it time to start
    
    if context.server_process.poll() is not None:
        error_message = "Angular server failed to start. \n"
        if context.server_process.returncode == 0:
            error_message += "Process exited successfully but shouldn't have.\n"
        else:
            error_message += f"Process exited with return code {context.server_process.returncode} \n"
        raise RuntimeError(error_message)


def after_all(context):
    """Stop the Angular app after tests complete."""
    context.server_process.terminate()