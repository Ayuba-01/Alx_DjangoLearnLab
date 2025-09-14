from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import BookSearchForm
from .models import CustomUser, Book

@permission_required("bookshelf.can_create", raise_exception=True)
def add_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        date_of_birth = request.POST.get("date_of_birth")
        profile_photo = request.POST.get("profile_photo")
        CustomUser.objects.create(email=email, date_of_birth=date_of_birth, profile_photo=profile_photo)
        return redirect("bookshelf:list_user") 
    users = CustomUser.objects.all()
    return render(request, "bookshelf/add_user.html", {"users": users})


@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        email = request.POST.get("email")
        date_of_birth = request.POST.get("date_of_birth")
        profile_photo = request.POST.get("profile_photo")
        if email:
            user.email = email
        if date_of_birth:
            user.date_of_birth = date_of_birth
        if profile_photo:
            user.profile_photo = profile_photo
        user.save()
        return redirect("bookshelf:list_users")
    users = CustomUser.objects.all()
    return render(request, "relationship_app/edit_book.html", {"user": users})


@permission_required("bookshelf.Can Delete", "bookshelf.can_view", raise_exception=True)
def delete_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect("bookshelf:list_users")
    return render(request, "bookshelf/confirm_delete_user.html", {"book": user})


@permission_required("bookshelf.can_create", "bookshelf.can_view", raise_exception=True)
def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        Book.objects.create(title=title, author=author)
        return redirect("bookshelf:book_list") 
    books = Book.objects.all()
    return render(request, "bookshelf/add_book.html", {"authors": books})


@permission_required("bookshelf.can_edit", "bookshelf.can_view",raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        title = request.POST.get("title")
        author= request.POST.get("author")
        if title:
            book.title = title
        if author:
            book.author = author
        book.save()
        return redirect("bookshelf:list_books")
    books = Book.objects.all()
    return render(request, "bookshelf/edit_book.html", {"book": books})


@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("bookshelf:list_books")
    return render(request, "bookshelf/confirm_delete_book.html", {"book": book})


def search_books(request):
    form = BookSearchForm(request.GET or None)
    qs = Book.objects.select_related("author")  # efficient join; still safe

    if form.is_valid():
        q = form.cleaned_data.get("q")
        author = form.cleaned_data.get("author")
        order = form.cleaned_data.get("order") or "title"

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(author__name__icontains=q))
        if author:
            qs = qs.filter(author__name__icontains=author)

        # Whitelist order fields (avoid user-controlled order_by injection)
        allowed_orders = {"title", "-title", "author__name", "-author__name"}
        if order in allowed_orders:
            qs = qs.order_by(order)

    # Pagination also protects you from accidental huge responses
    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "relationship_app/book_search.html",
        {"form": form, "page_obj": page_obj},
    )