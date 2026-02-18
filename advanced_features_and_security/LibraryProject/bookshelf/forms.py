from django import forms
from .models import Book


class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description']

    def clean_title(self):
        """Custom validation for title field"""
        title = self.cleaned_data.get('title')
        if len(title) < 2:
            raise forms.ValidationError("Title must be at least 2 characters long.")
        return title

    def clean_author(self):
        """Custom validation for author field"""
        author = self.cleaned_data.get('author')
        if len(author) < 2:
            raise forms.ValidationError("Author name must be at least 2 characters long.")
        return author