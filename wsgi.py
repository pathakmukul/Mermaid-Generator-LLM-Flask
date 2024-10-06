import importlib.util
import os
import sys

# Add the path of your project to sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Load the module from mermaid.py using importlib
spec = importlib.util.spec_from_file_location("mermaid", "/home/aneksbjl/flow1/mermaid.py")
mermaid = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mermaid)

# Set the application variable for WSGI
application = mermaid.app
