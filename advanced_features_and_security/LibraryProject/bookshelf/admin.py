from django.contrib import admin

from .models import Book
from .models import CustomUser

class BookAdmin(admin.ModelAdmin):
    list_filter = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author', 'publication_year')

admin.site.register(Book)


class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ('date_of_birth', 'email')
    search_fields = ('date_of_birth', 'email')
    
admin.site.register(CustomUser, CustomUserAdmin)
