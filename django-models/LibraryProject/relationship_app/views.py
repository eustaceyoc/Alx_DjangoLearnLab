from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library

# Function-based view: simple text list of all books
def list_books(request):
    books = Book.objects.all()
    lines = [f"{book.title} by {book.author.name}" for book in books]
    return HttpResponse("\n".join(lines), content_type="text/plain")

# Class-based view: display details of a specific library (HTML)
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'
