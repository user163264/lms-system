# /home/ubuntu/lms/backend/app/routes/__init__.py
# This file can remain empty or include shared route components

"""
Routes package for API endpoints
"""
# Make sure we can import our new router
import importlib
import os

# Import existing routers from the current package
from . import lessons, exercises, users