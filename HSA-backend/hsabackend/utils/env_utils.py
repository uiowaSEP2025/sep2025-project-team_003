import os

def get_url():
    if "ENV" not in os.environ:
        return "http://localhost:4200"
    if os.environ["ENV"] == "DEV":
        return "https://hsa.ssankey.com"
    if os.environ["ENV"] == "PROD":
        return "https://hsa-app.starlitex.com"
    else:
        raise RuntimeError("The enviornment for the backend was not set correctly")
