from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework import filters
from django_filters import rest_framework


class BookListView(generics.ListAPIView):
    """
    GET /books/ — list all books
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # --- Filtering (structured) ---
    filterset_fields = {
        'title': ['exact', 'icontains'],
        'publication_year': ['exact', 'gte', 'lte'],
        'author': ['exact'],                 # by author ID: ?author=3
        'author__name': ['exact', 'icontains'],  # by author name
    }

    # --- Search (free text across fields) ---
    search_fields = ['title', 'author__name']    # NOT 'author_name' and not year

    # --- Ordering ---
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # optional default


class BookDetailView(generics.RetrieveAPIView):
    """
    GET /books/<pk>/ — retrieve a single book by ID
    """
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # lookup_field = 'pk'  # default; only change if your URL uses a different name


class BookCreateView(generics.CreateAPIView):
    """
    POST /books/ — create a new book
    """
    queryset = Book.objects.all()         # optional for CreateAPIView, but safe to include
    serializer_class = BookSerializer     # uses your validation (e.g., publication_year)
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, FormParser, MultiPartParser]


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /books/<pk>/ — update an existing book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, FormParser, MultiPartParser]



class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /books/<pk>/ — delete a book
    """
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]
    # serializer_class not required for DestroyAPIView
