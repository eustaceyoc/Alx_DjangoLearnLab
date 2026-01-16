# `delete.md`

```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")  # or "1984" if not updated
book.delete()
Book.objects.all()
