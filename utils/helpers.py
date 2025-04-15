import os
import webbrowser

def launch_app(path):
    try:
        if path.startswith(('http://', 'https://')):
            webbrowser.open(path)
        else:
            os.startfile(path)
        return True
    except Exception as e:
        return str(e)

def validate_image(path):
    if not path:
        return True
    return os.path.exists(path) and path.lower().endswith(('.png', '.jpg', '.jpeg', '.ico'))

def validate_executable(path):
    if not path:
        return False
    return os.path.exists(path) or path.startswith(('http://', 'https://'))