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
        # Users
        cls.user = User.objects.create_user(username="alice", password="alicepass")
        cls.other = User.objects.create_user(username="bob", password="bobpass")

        # Tokens
        cls.user_token = Token.objects.create(user=cls.user)
        cls.other_token = Token.objects.create(user=cls.other)

        # Data
        cls.a1 = Author.objects.create(name="J.R.R. Tolkien")
        cls.a2 = Author.objects.create(name="Chinua Achebe")

        cls.b1 = Book.objects.create(title="The Hobbit", publication_year=1937, author=cls.a1)
        cls.b2 = Book.objects.create(title="The Lord of the Rings", publication_year=1954, author=cls.a1)
        cls.b3 = Book.objects.create(title="Things Fall Apart", publication_year=1958, author=cls.a2)

    # --- helpers ---
    def client_auth(self, token):
        c = APIClient()
        c.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        return c

    # ---------- CRUD ----------
    def test_list_books_public_ok(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 3)

    def test_detail_book_public_ok(self):
        url = reverse("book-detail", args=[self.b1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "The Hobbit")

    def test_detail_book_not_found(self):
        url = reverse("book-detail", args=[999999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_book_requiresponse_auth(self):
        url = reverse("book-create")
        payload = {"title": "No Token Book", "publication_year": 2020, "author": self.a1.id}
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_with_auth_201(self):
        url = reverse("book-create")
        payload = {"title": "Half of a Yellow Sun", "publication_year": 2006, "author": self.a2.id}
        response = self.client_auth(self.user_token).post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Half of a Yellow Sun")

    def test_update_book_with_future_year_400(self):
        url = reverse("book-update", args=[self.b1.pk])
        payload = {"publication_year": 9999}
        response = self.client_auth(self.user_token).patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Optional: assert error key exists
        # self.assertIn("publication_year", response.data)

    def test_update_book_ok(self):
        url = reverse("book-update", args=[self.b1.pk])
        payload = {"title": "The Hobbit (Updated)"}
        response = self.client_auth(self.user_token).patch(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # verify persisted
        self.b1.refresponseh_from_db()
        self.assertEqual(self.b1.title, "The Hobbit (Updated)")

    def test_delete_book_requiresponse_auth(self):
        url = reverse("book-delete", args=[self.b2.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_204(self):
        url = reverse("book-delete", args=[self.b2.pk])
        response = self.client_auth(self.user_token).delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.b2.pk).exists())

    # ---------- Filtering ----------
    def test_filter_by_author_id(self):
        url = reverse("book-list")
        response = self.client.get(url, {"author": self.a1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertListEqual(sorted(titles), sorted(["The Hobbit", "The Lord of the Rings"]))

    def test_filter_by_year_range(self):
        url = reverse("book-list")
        response = self.client.get(url, {"publication_year__gte": 1950, "publication_year__lte": 1960})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in response.data]
        self.assertTrue(all(1950 <= y <= 1960 for y in years))

    def test_filter_title_contains(self):
        url = reverse("book-list")
        response = self.client.get(url, {"title__icontains": "lord"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Lord" in b["title"] for b in response.data))

    # ---------- Search ----------
    def test_search_by_author_name(self):
        url = reverse("book-list")
        response = self.client.get(url, {"search": "tolkien"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all("tolkien" in b["author"]["name"].lower() for b in response.data))

    # ---------- Ordering ----------
    def test_ordering_by_title_asc(self):
        url = reverse("book-list")
        response = self.client.get(url, {"ordering": "title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_ordering_by_year_desc(self):
        url = reverse("book-list")
        response = self.client.get(url, {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
