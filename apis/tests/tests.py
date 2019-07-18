
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from books.models import Book, Category
from students.models import Student

class BookTests(APITestCase):
    def test_create_book(self):
        """
        Ensure we can create a new Book object.
        """
        category = Category.objects.filter(id=1).first()
        print(category)
        student = Student.objects.first()
        Book.objects.create(id=100, title= "test Book 10", category=category, status='sale', image='#', available = True, owner=student)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        # self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.filter(title='test Book 10').first().title, 'test Book 10')
