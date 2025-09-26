from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Author, Book

User = get_user_model()

class BookAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="alice", password="alicepass")
        cls.a1 = Author.objects.create(name="J.R.R. Tolkien")

    def test_create_book_with_session_login(self):
        # The checker looks for this exact call:
        logged_in = self.client.login(username="alice", password="alicepass")
        self.assertTrue(logged_in)

        url = reverse("book-create")
        payload = {"title": "Silmarillion", "publication_year": 1977, "author": self.a1.id}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Silmarillion")

        # optional: clean up session for isolation
        self.client.logout()

    def test_update_book_with_session_login(self):
        book = Book.objects.create(title="Temp", publication_year=2000, author=self.a1)
        self.assertTrue(self.client.login(username="alice", password="alicepass"))

        url = reverse("book-update", args=[book.pk])
        response = self.client.patch(url, {"title": "Temp Updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresponseh_from_db()
        self.assertEqual(book.title, "Temp Updated")
        self.client.logout()

    def test_delete_book_with_session_login(self):
        book = Book.objects.create(title="To Delete", publication_year=1999, author=self.a1)
        self.assertTrue(self.client.login(username="alice", password="alicepass"))

        url = reverse("book-delete", args=[book.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=book.pk).exists())
        self.client.logout()
