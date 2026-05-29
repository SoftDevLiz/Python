from django.contrib import admin
from .models import Note  # Import your Note model

# This makes it appear in the admin panel
admin.site.register(Note)
