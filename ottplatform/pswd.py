# generate_password_hash.py

import os
import django
from django.conf import settings
from django.contrib.auth.hashers import make_password

# Set the environment variable to point to your Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ottplatform.settings')

# Initialize Django
django.setup()

# Replace with the desired password
password = "friends"

# Generate hashed password
hashed_password = make_password(password)
print("Hashed Password:", hashed_password)