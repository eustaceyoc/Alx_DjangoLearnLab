from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create authors
        self.author1 = Author.objects.create(name="J.K. Rowling")
        self.author2 = Author.objects.create(name="George Orwell")

        # Create books
        self.book1 = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author1)
        self.book2 = Book.objects.create(title="1984", publication_year=1949, author=self.author2)

        # Initialize API client
        self.client = APIClient()

    # READ: List and Detail
    def test_list_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two books created

    def test_retrieve_book(self):
        response = self.client.get(f'/api/books/{self.book1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Harry Potter")

    # CREATE
    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')  # login required for creation
        data = {
            'title': 'Animal Farm',
            'publication_year': 1945,
            'author': self.author2.id
        }
        response = self.client.post('/api/books/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        data = {
            'title': 'Unauth Book',
            'publication_year': 2020,
            'author': self.author1.id
        }
        response = self.client.post('/api/books/create/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # UPDATE
    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        data = {'title': 'Harry Potter Updated', 'publication_year': 1998, 'author': self.author1.id}
        response = self.client.put(f'/api/books/{self.book1.id}/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Harry Potter Updated')

    # DELETE
    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(f'/api/books/{self.book2.id}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    # FILTERING
    def test_filter_books_by_title(self):
        response = self.client.get('/api/books/?title=Harry Potter')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Harry Potter')

    # SEARCH
    def test_search_books_by_author(self):
        response = self.client.get('/api/books/?search=Orwell')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    # ORDERING
    def test_order_books_by_publication_year_desc(self):
        response = self.client.get('/api/books/?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 1997)
