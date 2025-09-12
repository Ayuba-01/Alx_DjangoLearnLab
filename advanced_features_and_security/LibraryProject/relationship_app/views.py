from django.shortcuts import render
from .models import Book, Author
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate
from .models import UserProfile
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404

def list_books(request):
    books = Book.objects.all()
    context = {"book_list": books}
    
    return render(request, "relationship_app/list_books.html", context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
    

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

def login_view_minimal(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("relationship_app:list_books")
        else:
            return render(request, "relationship_app/login.html", {"error": "Invalid credentials"})
    return render(request, "relationship_app/login.html")


def register(request):
    """
    Simple registration using Django's built-in UserCreationForm.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect("relationship_app:login")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


def _is_admin(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.role == UserProfile.role("admin")
    )

@user_passes_test(_is_admin, login_url="relationship_app:login")
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


def _is_member(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.role == UserProfile.Roles.MEMBER
    )

@user_passes_test(_is_member, login_url="relationship_app:login")
def member_view(request):
    return render(request, "relationship_app/member_view.html")

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .models import UserProfile

def _is_librarian(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.role == UserProfile.Roles.LIBRARIAN
    )

@user_passes_test(_is_librarian, login_url="relationship_app:login")
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@permission_required("relationship_app.can_add_book", raise_exception=True)
def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author_id = request.POST.get("author_id")
        author = get_object_or_404(Author, pk=author_id)
        Book.objects.create(title=title, author=author)
        return redirect("relationship_app:list_books") 
    authors = Author.objects.all()
    return render(request, "relationship_app/add_book.html", {"authors": authors})


@permission_required("relationship_app.can_change_book", raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        title = request.POST.get("title")
        author_id = request.POST.get("author_id")
        if title:
            book.title = title
        if author_id:
            book.author = get_object_or_404(Author, pk=author_id)
        book.save()
        return redirect("relationship_app:list_books")
    authors = Author.objects.all()
    return render(request, "relationship_app/edit_book.html", {"book": book, "authors": authors})


@permission_required("relationship_app.can_delete_book", raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("relationship_app:list_books")
    return render(request, "relationship_app/confirm_delete_book.html", {"book": book})
