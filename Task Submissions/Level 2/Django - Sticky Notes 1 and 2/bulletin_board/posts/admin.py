from django.contrib import admin
from .models import Post
from .models import Author

# Register your models here.

# Post model
admin.site.register(Post)

# Author model
admin.site.register(Author)
