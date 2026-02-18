from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.db.models import Q
from .models import Book, Library
from .forms import ExampleForm


@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    search_query = request.GET.get('search', '').strip()

    if search_query:
        books = Book.objects.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        )
    else:
        books = Book.objects.all()

    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'search_query': search_query
    })


@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Secure creation using Django ORM with validated data
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('book_list')
    else:
        form = ExampleForm()

    return render(request, 'bookshelf/form_example.html', {'form': form})


@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.created_by != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You can only edit books you created.")

    if request.method == 'POST':
        form = ExampleForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_list')
    else:
        form = ExampleForm(instance=book)

    return render(request, 'bookshelf/form_example.html', {'form': form, 'book': book})

@login_required
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if book.created_by != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You can only delete books you created.")

    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('book_list')

    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


@login_required
@permission_required('bookshelf.can_view_library', raise_exception=True)
def library_list(request):
    libraries = Library.objects.all()
    return render(request, 'bookshelf/library_list.html', {'libraries': libraries})


def user_dashboard(request):
    user_books = Book.objects.filter(created_by=request.user)
    user_permissions = request.user.get_all_permissions()

    return render(request, 'bookshelf/dashboard.html', {
        'user_books': user_books,
        'user_permissions': user_permissions
    })
