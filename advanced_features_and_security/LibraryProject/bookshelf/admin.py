from django.contrib import admin
from .models import Book

# Customize admin display for Book model
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns shown in list view
    list_filter = ('publication_year', 'author')            # Filter sidebar
    search_fields = ('title', 'author')                     # Search box

# Register the model with custom admin
admin.site.register(Book, BookAdmin)