from django.contrib import admin
from bookBank.models import (books,subjects,author)
# Register your models here.

admin.site.register(books)
admin.site.register(subjects)
admin.site.register(author)

